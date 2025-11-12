import os

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Lookup filter
app.jinja_env.filters["lookup"] = lookup

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # get users portfolio from databse
    portfolio = db.execute("""
    SELECT
        stocks.symbol,
        stocks.name,
        SUM(purchase.quantity) AS total_quantity,
        stocks.price,
        SUM(purchase.quantity * stocks.price) AS total_value,
        owned_shares.quantity_owned
    FROM purchase
    JOIN stocks ON stocks.id = purchase.stockID
    JOIN owned_shares ON stocks.id = owned_shares.stockID
    WHERE purchase.userID = ?
    GROUP BY stocks.id
""", session["user_id"])

    # calculate value of all stocks
    total_assests_value = sum(stock["total_value"] for stock in portfolio if stock["total_value"])
    # get portfolio owner's username
    user_name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    # get user's cash balance
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    # calculate user's total net worth
    net_worth = total_assests_value + user_cash
    return render_template("layout.html", portfolio=portfolio, net_worth=net_worth, user_cash=user_cash, user_name=user_name)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add():
    """Add Cash"""
    if request.method == "POST":
        if not request.form.get("cash"):
            flash("Eneter the amount of cash to ass", "error 409")
            return redirect("/add_cash")
        # check if the amount is not negative
        if int(request.form.get("cash")) < 0:
            flash("The amount can't be a negative number ", "error 421")
            return redirect("/add_cash")
        # add cash and render a return message
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                   request.form.get("cash"), session["user_id"])
        flash(
            f"Successfully added {request.form.get("cash")} to {session["user_id"]} account!", "success")
        return render_template("add_cash.html")

    else:
        return render_template("add_cash.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Check if symbol was eneterd
        if not request.form.get("symbol"):
            flash("Symbol is required!", "error 401")
            return redirect("/buy", 400)


        # Check if no. of shares to buy is entered
        if not request.form.get("shares"):
            flash("must provide number of shares", "error 402")
            return redirect("/buy", 400)


         #check if no. shares in not fractional
        try:
            shares_quantity = int(request.form.get("shares"))
        except ValueError:
            flash("Number of shares can't be fractional", "error 402")
            return redirect("/buy", 400)

        # Check if no. of shares to buy is positvie
        if shares_quantity <= 0:
            flash("Number shares must be a positive integer", "error 402")
            return redirect("/buy", 400)


        # Search the stock
        stock = lookup(request.form.get("symbol"))
        if not stock:
            flash("Invalid symbol", "error 402")
            return redirect("/buy", 400)

        # Get user's cash, stock's price and quantity and caluclate total cost
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        stock_price = stock["price"]
        total = float(shares_quantity) * stock_price

        # Check if cost does not exceed user's cash
        if user_cash < total:
            flash("insufficient", "error 504")
            return redirect("/buy", 400)

        # Get the date of the purchase
        date = datetime.now()

        # Check if stock is already in stocks tabel
        existing_stock = db.execute("SELECT * FROM stocks WHERE name = ?", stock["name"])

        if existing_stock:
            # update the price
            db.execute("UPDATE stocks SET price = ? WHERE name = ?", stock_price, stock["name"])
        else:
            # insert new stock data
            db.execute("INSERT INTO stocks (name, price, symbol) VALUES (?, ?, ?)",
                       stock["name"], stock_price, stock["symbol"])

        # Insert purchase data into purchase table
        db.execute(
            "INSERT INTO purchase (userID, stockID, quantity, date, type) "
            "VALUES ("
            "(SELECT id FROM users WHERE id = ?), "
            "(SELECT id FROM stocks WHERE name = ?),"
            "?, ?, ?)",
            session["user_id"],
            stock["name"],
            shares_quantity,
            date,
            "purchase"
        )

        # Check if stock is already in owned table
        existing_stock = db.execute(
            "SELECT * FROM owned_shares "
            "WHERE userID = ? AND stockID = (SELECT id FROM stocks WHERE name = ?)",
            session["user_id"],
            stock["name"]
        )
        if existing_stock:
            db.execute(
                "UPDATE owned_shares "
                "SET quantity_owned = quantity_owned + ? "
                "WHERE userID = ? "
                "AND stockID = (SELECT id FROM stocks WHERE name = ?)",
                shares_quantity,
                session["user_id"],
                stock["name"]
            )
        else:
            # Insert purchase data into owned_shares table
            db.execute(
                "INSERT INTO owned_shares (userID, stockID, quantity_owned) "
                "VALUES (?, (SELECT id FROM stocks WHERE name = ?), ?)",
                session["user_id"],
                stock["name"],
                shares_quantity
            )

        # susbtract value of the purchase from their cash balance
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash - total, session["user_id"])

        flash(
            f"Successfully bought {request.form.get("shares")} shares of {request.form.get("symbol")}!", "success")
        return redirect("/")


    return render_template("buy.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change password"""
    if request.method == "GET":
        return render_template("change.html")

    if request.method == "POST":

        # check if the username was enetered
        if not request.form.get("username"):
            flash("Username required", 404)
            return redirect("/change_password")
        # check if userename is registered
        users = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if not users:
            flash("No user of the username", 504)
            return redirect("/change_password")
        # check if the old password was enetered
        if not request.form.get("old_pass"):
            flash("Enetr old password", 404)
            return redirect("/change_password")
        # check if user confirmed password
        if not request.form.get("new_pass"):
            flash("Enter new password", 404)
            return redirect("/change_password")
        # check if passwords are idenitical
        if request.form.get("old_pass") == request.form.get("new_pass"):
            flash("Old password and new password can't be identical", 404)
            return redirect("/change_password")
        # hask password
        new_hashed_password = generate_password_hash(request.form.get("new_pass"))
        # Insert new password into the databse
        db.execute("UPDATE users SET hash = ? WHERE username = ?",
                   new_hashed_password, request.form.get("username"))
        flash("Password changed succesfully", success)
        return render_template("change.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transaction_history = db.execute("SELECT "
                                     "stocks.name, "
                                     "stocks.price, "
                                     "stocks.symbol, "
                                     "purchase.quantity, "
                                     "purchase.date, "
                                     "purchase.type "
                                     "FROM purchase "
                                     "JOIN stocks "
                                     "ON stocks.id = purchase.stockID "
                                     "WHERE purchase.userID = ? "
                                     "ORDER BY purchase.date DESC ",
                                     session["user_id"])

    if not transaction_history:
        flash("No transactions found!", "error 603")
        return redirect("/buy", 400)
    return render_template("history.html", transaction_history=transaction_history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Username required!", "error")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Password required!", "error")
            return redirect("/login")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("invalid username and/or password", 403)
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    elif request.method == "POST":
        if not request.form.get("symbol"):
            flash("Enter the stock symbol", 405)
            return redirect("/quote", 400)

        # serch for the stock
        stock = lookup(request.form.get("symbol"))

        # check if the stock was found
        if not stock:
            flash("Stock not found", 405)
            return redirect("/quote", 400)

        return render_template("quoted.html", stock=stock)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # check if the username was enetered
        if not request.form.get("username"):
            flash("Username required", 404)
            return redirect("/register", 400)
        # check if the password was enetered
        if not request.form.get("password"):
            flash("Username password", 404)
            return redirect("/register", 400)
        # check if user confirmed password
        if not request.form.get("confirmation"):
            flash("Password must be confirmed", 404)
            return redirect("/register", 400)
        # check if passwords are idenitical
        if request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords must be Identical", 404)
            return redirect("/register", 400)
        # hask password
        hashed_password = generate_password_hash(request.form.get("password"))
        # Insert user's login and hashed password into the databse and check if username is taken
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)",
                       request.form.get("username"), hashed_password)
        except ValueError:
            flash("This username already exists", 404)
            return redirect("/register", 400)

        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # check id symblol was eneterd
        if not request.form.get("symbol"):
            flash("Symbol is required!", "error 401")
            return redirect("/sell", 400)
        # check if number of shares to buy was entered correctly
        if not request.form.get("shares") or int(request.form.get("shares")) < 0:
            flash("Number of shares must can't be a negative number", 406)
            return redirect("/sell", 400)
        # search for the stock
        stock = lookup(request.form.get("symbol"))
        if not stock:
            flash("Stock not found", 404)
            return redirect("/sell", 400)

        owned_shares_no = db.execute(
            "SELECT quantity_owned FROM owned_shares "
            "WHERE userID = ? "
            "AND stockID = (SELECT id FROM stocks WHERE name = ?)",
            session["user_id"],
            stock["name"]
        )[0]["quantity_owned"]


        # check if shares number in transaction does not exceed the number owned shares
        shares_quantity = request.form.get("shares")
        if int(shares_quantity) > int(owned_shares_no):
            flash("You cannot sell more shares than you own", 404)
            return redirect("/sell", 400)

        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        # get the price of the stock and calcuate total cost
        stock_price = stock["price"]
        total = float(shares_quantity) * stock_price

        # get the date of the transaction
        date = datetime.now()

        # check if users owns the stock
        if owned_shares_no:
            db.execute("UPDATE stocks SET price = ? WHERE name = ?", stock_price, stock["name"])
        else:
            flash("You don't own this stock", 404)
            return redirect("/sell", 400)

        # insert the data of the sell into purchase table
        db.execute(
            "INSERT INTO purchase (userID, stockID, quantity, date, type) "
            "VALUES ( "
            "(SELECT id FROM users WHERE id = ?), "
            "(SELECT id FROM stocks WHERE name = ?),"
            "?, ?, ?)",
            session["user_id"],
            stock["name"],
            shares_quantity,
            date,
            "sell"
        )

        # update owned shares
        db.execute(
            "UPDATE owned_shares "
            "SET quantity_owned = quantity_owned - ? "
            "WHERE userID = ? "
            "AND stockID = (SELECT id FROM stocks WHERE name = ?)",
            shares_quantity,
            session["user_id"],
            stock["name"]
        )

        # delete the data from owned shares if the quantity equals 0
        db.execute(
            "DELETE FROM owned_shares "
            "WHERE userID = ? "
            "AND stockID = (SELECT id FROM stocks WHERE name = ?)"
            "AND quantity_owned = 0",
            session["user_id"],
            stock["name"]
        )

        # update users cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   user_cash + total, session["user_id"])
        flash(
            f"Successfully sold {request.form.get("shares")} shares of {request.form.get("symbol")}!", "success")
        return redirect("/")

    #get user's stocks for select input
    owned_stocks = db.execute(
    "SELECT stocks.symbol "
    "FROM owned_shares "
    "JOIN stocks ON owned_shares.stockID = stocks.id "
    "WHERE owned_shares.userID = ?",
    session["user_id"]
    )
    return render_template("sell.html", owned_stocks = owned_stocks)

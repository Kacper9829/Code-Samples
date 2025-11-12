# EXPENSE TRACKER
#### Video Demo:  <[URL HERE](https://youtu.be/X6E6fbF1MY0)>
### Description:
### Overview
**Expense Tracker** is an app designed to track users expenses and provide statistics on their finances, built in **Python** with **Flask framework** and **SQLAlchemy ORM**. Expense Tracker uses **postgresSQL**, an open source object-relational database system, to store users data. Tables in database were created with SQLAlchemy Object-Relational Mapping. 

### Structure

1. Configuration files
 The main application is run from **app.py**, where all routes are imported and registered using **flask blueprints**. The **app.py** also sets up **flask LoginManager**, the database and SQLAlchemy, that is configured in the **config.py** file (connected to postgresSQL). Migration are done using **flask Migrate** and set up in **manage.py** file.
2. Database ORM models
Models located in **models.py** create four tables:
- **User** table that contains rows for: 
     - id  the primary_key
     - username 
     - first-name 
     - email 
     - password_hash (hashed using werkzeug.security)
     - expenses (with foreign key and relationship to **Expense** table and with **cascade** option to delete user with all his expenses)
     - user_default_currency and user_default_currency_id (user chooses during registration, with foreign key and relationship **currency table**)
     - is_admin row that determines whether user is an admin
- **Expense** table that contains rows for:
     - id the primary_key
     - user_id (with foreign key to **user** table)
     - amount
     - category and category_id(with foreign key and relationship to **category** table)
     - currency and currency_id (with foreign key and relationship to **currency** table)
     - date
     - description
- **Category**
     - id the primary_key
     - name
- **Currency**
     - id the primary_key
     - code 
     - name 
     - exchange_rate_to_euro
3. **seed_categories.py** and **seed_currencies** are python files used to seed database with default currencies and categories for expenses. Usage in terminal: **python file_name**.
4. **helpers.py** contain two helpers function for calculating monthly average expanses and updating currency rates with API, respectively.
5. **the templates folder** contains templates for html pages of the application design using Bootstrap framework and with Copilot assistance for graphical design and color.
6. **static** folder contains the css stylesheet design on the basis of free online sources like W3Schools and Dev Snap
7. **routes** folder contains 5 files containing route flask blueprints:
    - **users.py** contains route blueprint for login, using LoginManger, register, and logout user as well as the main page dashboard, displaying most recent expenses, functions.
    - **stats.py** contains route blueprint for function calculating statistics of users finances and expenses, such as total expenses for selected year, monthly average, and expenses per category.
    - **settings.py** contains route blueprint for functions changing current user's username, password and default currency, as well as admin only function for updating currency rates using helpers function update_currencies.
    - **expense.py** contains route blueprint for functions adding new expenses, deleting and editing them.
    - **history.py** contains route blueprint for function displaying expenses for selected year.

### Technologies and solutions used

1. **Flask** a open-source web framework for Python, that handles routing and requesting in my project. It's also enable me to use flask SQLAlchemy ORM and migration of data in database using FlaskMigrate. It's simple and lightweight and perfect for creating application, while still learning new things. 
    - **Flask Migrate** uses Alembic to handle SQLAlchemy database migrations.
    - **Flask blueprints** great for large applications with many routes to keep main **app.py** cleaner and more readable.
    - **Flask LoginManger** used to log in and log out users, as well as enabling useful functions like current_user or login_required. 
2. **SQLAlchemy ORM** While making this CS50 final project I opted for using SQLAlchemy ORM as its a great way to design qnd operate on a database, as well as an opportunity to learn new things, other than simple SQL and SQLite. The SQL syntax basics combined with python programming knowledge makes SQLAlchemy a really useful tool for clean and simple queries.
3. **PostgreSQL** Similarly to **SQLAlchemy ORM**, I have chosen **PostgreSQL** as an upgrade from ****SQLite**, more advanced and commonly used database system with better concurrency, scaling, and data integrity.
4. **Bootstrap** adds more polished looking HTML and CSS to make the app more presentable.

### Usage

1. The Expense Tracker app allows to register an account in the database, entering their first-name, username, email, password and default currency, in which their financial statistics will be displayed.
2. After registering and logging in, users will see their most recent (90days) expenses, that they can edit or delete. From main dashboard users have access to routes to add expense, display statistics of their finances, history of their expenses as well as settings.
3. Main Functions:
    -  **ADD EXPENSES** function allows adding new expense with amount, currency, category, date and description defined by the user.
    -  **STATISTICS** function displays user statistics like year total, monthly average, highest expense for selected years and a percentage comparisons with pervious year. **STATISTICS** also shows user total expenses per categories and monthly breakdown for a selected year.
    -  **HISTORY** function displays all the expenses for selected year.
    -  **SETTINGS** allows user to change his username, password, default currency and for administrator only, update currency.Users can also delete their account.
    -  **LOGOUT** allows user to logout.




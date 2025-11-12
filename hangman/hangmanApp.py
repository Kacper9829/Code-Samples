from PyQt5.QtGui import QKeySequence, QRegExpValidator, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QMessageBox, QCalendarWidget, QShortcut, QLabel, QFormLayout
from PyQt5.QtCore import QRegExp
import sys
import random


class hangman(QMainWindow):

    def __init__(self):
        super().__init__()
        self.word_list = [line.strip() for line in open("words.txt", 'r')]
        self.word = random.choice(self.word_list)
        self.guessed_letters = set()
        self.total_attempts = 8
        self.setWindowTitle("Hangman")
        self.setGeometry(100, 100, 400, 400)
        self.set_up_UI()

    def set_up_UI(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        sub_layout = QFormLayout()
        main_layout.addLayout(sub_layout)

        self.letters_uncovered = QLabel(f"Guessed letters: {self.show_guessed_letters()}")
        main_layout.addWidget( self.letters_uncovered)

        self.input_letter = QLineEdit(self)
        reg_ex = QRegExp("[a-z-A-Z_]+")
        self.input_validator = QRegExpValidator(reg_ex, self.input_letter)
        self.input_letter.setMaxLength(1)
        self.input_letter.setValidator(self.input_validator)

        self.image = QLabel(self)
        self.pixmap = QPixmap(r"C:\Users\kacpe\Desktop\python\projekty\hangman\1.jpg")
        self.image.setPixmap(self.pixmap)
        main_layout.addWidget(self.image)

        guess_button = QPushButton("Guess", self)
        guess_button.clicked.connect(self.guess_letter)
        guess_button.setShortcut("Return")
        main_layout.addWidget(guess_button)

        change_button = QPushButton("New word")
        change_button.clicked.connect(self.choose_new_word)
        change_button.setShortcut("Tab")
        main_layout.addWidget(change_button)

        sub_layout.addRow(QLabel("Guess a letter"), self.input_letter)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget) 

    def attempts(self):
        self.total_attempts -= 1
        if self.total_attempts == 0:
            QMessageBox.information(self, "Game over", f"You've lost the game. The word was {self.word}")
        elif self.total_attempts == 7:
            self.image.setPixmap(QPixmap(r"C:\Users\kacpe\Desktop\python\projekty\hangman\2.jpg"))
        elif self.total_attempts == 6:
            self.image.setPixmap(QPixmap(r"C:\Users\kacpe\Desktop\python\projekty\hangman\3.jpg"))
        elif self.total_attempts == 5:
            self.image.setPixmap(QPixmap(r"C:\Users\kacpe\Desktop\python\projekty\hangman\4.jpg"))
        elif self.total_attempts == 4:
            self.image.setPixmap(QPixmap(r"C:\Users\kacpe\Desktop\python\projekty\hangman\5.jpg"))
        elif self.total_attempts == 3:
            self.image.setPixmap(QPixmap(r"C:\Users\kacpe\Desktop\python\projekty\hangman\6.jpg"))
        elif self.total_attempts == 2:
            self.image.setPixmap(QPixmap(r"C:\Users\kacpe\Desktop\python\projekty\hangman\7.jpg"))
        elif self.total_attempts == 1:
            self.image.setPixmap(QPixmap(r"C:\Users\kacpe\Desktop\python\projekty\hangman\8.jpg"))

    def choose_new_word(self):
        self.word = random.choice(self.word_list)
        self.image.setPixmap(QPixmap(r"C:\Users\kacpe\Desktop\python\projekty\hangman\1.jpg"))
        self.total_attempts = 8
        self.guessed_letters.clear()
        self.letters_uncovered.setText(f"Guessed letters: {self.show_guessed_letters()}")

    def show_guessed_letters(self):
        return ''.join([letter if letter in self.guessed_letters else "_" for letter in self.word])

    def guess_letter(self):
        letter = self.input_letter.text()
        if letter in self.word and letter not in self.guessed_letters:
            self.guessed_letters.add(letter)
            QMessageBox.information(self, "Guessed", f"Correct You've guessed the letter. {letter} ")
            self.letters_uncovered.setText(f"Guessed letters: {self.show_guessed_letters()}")
        else:
            self.attempts()
            QMessageBox.warning(self, "Wrong letter", f"Your guess was wrong. Attempts remaining: {self.total_attempts}")
        self.clear_input()

    def clear_input(self):
        self.input_letter.clear()


app = QApplication(sys.argv)
window = hangman()
window.show()
sys.exit(app.exec_()) 
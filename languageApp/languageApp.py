from PyQt5.QtGui import QKeySequence, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QMessageBox, QCalendarWidget, QShortcut, QLabel, QComboBox, QHBoxLayout, QListView, QMenuBar, QMenu, QStatusBar, QAction, QFileDialog
from PyQt5.QtCore import QRect, QStringListModel
import sys
import random
import json

class LanguageApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Language App")
        self.setGeometry(100, 100, 400, 400)
        self.learntWords = []
        self.words_to_learn = []
        self.appMode = "Learn"
        self.set_up_UI()

    def set_up_UI(self):

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        mainLayout = QHBoxLayout(self.centralwidget)
      
        self.verticalLayoutWidget_2 = QWidget()
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayoutWidget_2.setFixedSize(200, 500)

        self.labelWordList = QLabel("Learnt Words")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelWordList.setFont(font)
        self.verticalLayout_2.addWidget(self.labelWordList)

        self.listView = QListView()
        self.model = QStringListModel(self.learntWords)
        self.listView.setModel(self.model)
        self.listView.clicked.connect(self.on_item_clicked)
        self.verticalLayout_2.addWidget(self.listView)

        self.SaveButton = QPushButton("Save to File")
        self.SaveButton.clicked.connect(self.save_to_file)
        self.verticalLayout_2.addWidget(self.SaveButton)

        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.clear_list)
        self.verticalLayout_2.addWidget(self.clearButton)

        mainLayout.addWidget(self.verticalLayoutWidget_2)

        self.horizontalLayoutWidget = QWidget()
        self.horizontalLayout = QVBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayoutWidget.setFixedSize(400, 500)

        self.labelWord = QLabel("Word")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.labelWord.setFont(font)
        self.horizontalLayout.addWidget(self.labelWord)

        self.labelDefinition = QLabel("Definition")
        self.labelDefinition.setWordWrap(True)
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.labelDefinition.setFont(font)
        self.horizontalLayout.addWidget(self.labelDefinition)

        self.CheckButton = QPushButton("Check", self)
        self.CheckButton.clicked.connect(self.check)
        self.horizontalLayout.addWidget(self.CheckButton)

        self.CorrectButton = QPushButton("Show Correct Answer", self)
        self.CorrectButton.clicked.connect(self.show_correct_answer)
        self.horizontalLayout.addWidget(self.CorrectButton)

        mainLayout.addWidget(self.horizontalLayoutWidget)

        self.verticalLayoutWidget = QWidget()
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayoutWidget.setFixedSize(200, 500)

        self.NewWordButton = QPushButton("New Word", self)
        self.NewWordButton.clicked.connect(self.learn)
        self.verticalLayout.addWidget(self.NewWordButton)

        self.learntButton = QPushButton("Mark as Learnt", self)
        self.learntButton.clicked.connect(self.mark_as_learnt)
        self.verticalLayout.addWidget(self.learntButton)

        self.learModeButton = QPushButton("Learn Mode", self)
        self.learModeButton.clicked.connect(lambda: self.change_mode("Learn"))
        self.verticalLayout.addWidget(self.learModeButton)

        self.quizModeButton = QPushButton("Quiz Mode", self)
        self.quizModeButton.clicked.connect(lambda: self.change_mode("Quiz"))
        self.verticalLayout.addWidget(self.quizModeButton)

        mainLayout.addWidget(self.verticalLayoutWidget)
        
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        self.actionUpload_new_word_list = QAction("Upload New Word List", self)
        self.actionSave_to_learn_list_to_file = QAction("Save to File", self)

        file_menu.addAction(self.actionUpload_new_word_list)
        self.actionUpload_new_word_list.triggered.connect(self.upload_word_list)
        file_menu.addAction(self.actionSave_to_learn_list_to_file)
        self.actionSave_to_learn_list_to_file.triggered.connect(self.save_to_file)

   
    def learn(self):
        with open("languageApp\word_list.json", "r") as file:
            if file.read() == '': 
                QMessageBox.information(self, "No List Uploaded", "Word List is Empty. First Upload New WordList")
                return
            else:
                if self.appMode != "Learn":
                    self.change_mode("Learn")
                    with open("languageApp\word_list.json", "r") as f:
                        data = json.load(f)

                    self.new_word_to_learn = random.choice(data)
                    self.new_definition = self.new_word_to_learn["definition"]
                    if self.new_word_to_learn not in self.learntWords: 
                        self.update_label(self.new_word_to_learn["word"], self.new_definition)
                    else:
                        pass
                else:
                    with open("languageApp\word_list.json", "r") as f:
                        data = json.load(f)

                    self.new_word_to_learn = random.choice(data)
                    self.new_definition = self.new_word_to_learn["definition"]
                    if self.new_word_to_learn not in self.learntWords: 
                        self.update_label(self.new_word_to_learn["word"], self.new_definition)
                    else:
                        pass

    def mark_as_learnt(self):
        with open("languageApp\word_list.json", "r") as file:
            if file.read() == '': 
                QMessageBox.information(self, "No List Uploaded", "Word List is Empty. First Upload New WordList")
                return
            else:
                if not hasattr(self, 'new_word_to_learn') or not self.new_word_to_learn:
                    QMessageBox.information(self, "No Word Chosen", "No word has been selected")
                    return

                if self.new_word_to_learn in self.learntWords:
                    return  

                self.learntWords.append(self.new_word_to_learn)
                self.update_model()
    
    def change_mode(self, mode):
        with open("languageApp\word_list.json", "r") as file:
            if file.read() == '': 
                QMessageBox.information(self, "No List Uploaded", "Word List is Empty. First Upload New WordList")
                return
            else:
                if self.appMode == mode:
                    QMessageBox.information(self, "Mode Error", f"The app mode is already set to {self.appMode} mode")
                else:
                    self.appMode = mode
                    if self.appMode == "Quiz":
                        self.answer_field = QLineEdit(self)
                        self.answer_field.setPlaceholderText("Input correct word: ")
                        self.labelWord.deleteLater()
                        self.horizontalLayout.removeWidget(self.labelWord)
                        self.horizontalLayout.insertWidget(0, self.answer_field)
                    else:
                        self.labelWord = QLabel("Word")
                        font = QFont()
                        font.setPointSize(20)
                        font.setBold(True)
                        self.labelWord.setFont(font)
                        self.answer_field.deleteLater()
                        self.horizontalLayout.removeWidget(self.answer_field)
                        self.horizontalLayout.insertWidget(0, self.labelWord)
                        self.quiz()
        
    def quiz(self):
        with open("languageApp\word_list.json", "r") as file:
            if file.read() == '': 
                QMessageBox.information(self, "No List Uploaded", "Word List is Empty. First Upload New WordList")
                return
            else:
                with open("languageApp\word_list.json", "r") as f:
                    data = json.load(f)

                self.quiz_word = random.choice(data)
                self.labelDefinition.setText(self.quiz_word["definition"])
                if hasattr(self, "answer_field"):
                    self.answer_field.clear()
        
    def check(self):
        with open("languageApp\word_list.json", "r") as file:
            if file.read() == '': 
                QMessageBox.information(self, "No List Uploaded", "Word List is Empty. First Upload New WordList")
                return
            else:
                if self.answer_field.text().strip().lower() == self.quiz_word["word"].strip().lower():
                    QMessageBox.information(self, "Correct Answer", "Great!!! Correct Answer")
                    self.quiz()
                else:
                    QMessageBox.information(self, "Wrong Answer", "Wrong Answer! Try Again")

    def show_correct_answer(self):
        with open("languageApp\word_list.json", "r") as file:
            if file.read() == '': 
                QMessageBox.information(self, "No List Uploaded", "Word List is Empty. First Upload New WordList")
                return
            else:
                QMessageBox.information(self, "Correct Answer", f"The correct answer is {self.quiz_word["word"]}")
    
    def save_to_file(self):
        with open("saved_words.json", "w", encoding="utf-8") as f:
            json.dump(self.words_to_learn, f, ensure_ascii=False, indent=2)
        QMessageBox.information(self, "Saved to File", "New words saved to file")

    def clear_list(self):
        self.words_to_learn.clear()
        self.update_model()

    def on_item_clicked(self):
        self.update_label(self.new_word_to_learn["word"], self.new_definition)

    def update_label(self, word, definition):
        if isinstance(self.labelWord, QLabel):
            self.labelWord.setText(word)
            self.labelDefinition.setText(definition)
        elif isinstance(self.labelWord, QLineEdit):
            self.labelWord.setText("")
            self.labelDefinition.setText(definition)
    
    def update_model(self):
        word_list = [item["word"] for item in self.learntWords]
        self.model.setStringList(word_list)

    def convert_txt_to_json(self, source_file):
        word_list = []
        with open(source_file, 'r', encoding='utf-8') as file:
            for line in file:
                if '\t' in line:
                    word, definition = line.strip().split('\t', 1)
                    word_list.append({
                        "word": word.strip(),
                        "definition": definition.strip()
                    })

        with open("languageApp\word_list.json", 'w', encoding='utf-8') as json_file:
            json.dump(word_list, json_file, indent=4, ensure_ascii=False)


    def upload_word_list(self):
        with open("languageApp\word_list.json", 'w', encoding='utf-8') as f:
             f.truncate(0)
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", "All Files (*)"
        )
        if file_path:
           self.convert_txt_to_json(file_path) 
           QMessageBox.information(self, "File Uploaded", "New Word List Has Been Uploaded") 
        else:
           QMessageBox.information(self, "No File Chosen", "Please Chose a File Containing a New Word List") 


app = QApplication(sys.argv)
window = LanguageApp()
window.show()
sys.exit(app.exec_()) 
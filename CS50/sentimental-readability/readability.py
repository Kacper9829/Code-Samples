import re

class readability:
    def __init__(self):
        self.text = ""
        self.letter_count = 0
        self.sentence_count = 0
        self.word_count = 0

    # get user's input
    def get_text(self):
        return input("Enter text to evaluate: ")

    # count letters by summing only alphabetical characters
    def count_letters(self, text):
        self.letter_count = sum(char.isalpha() for char in text)
        return self.letter_count

    # count words by spliting text on whitespaces
    def count_words(self, text):
        self.word_count = len(text.split())
        return self.word_count

    # count sentcens with regex
    def count_sentences(self, text):
        self.sentence_count = re.findall(r'[^.!?]+[.!?]', text)
        # remove empty strings
        self.sentence_count = [s for s in self.sentence_count if s.strip()]
        return len(self.sentence_count)

    # calcualte readablity
    def calculate_readability(self):
        self.text = self.get_text()
        L = (self.count_letters(self.text)/self.count_words(self.text))*100
        S = (self.count_sentences(self.text)/self.count_words(self.text))*100
        index = 0.0588 * L - 0.296 * S - 15.8
        if (index < 1):

            print("Before Grade 1\n")

        elif (index > 16):

            print("Grade 16+\n")

        else:

            int_index = round(index)
            print(f"Grade {int_index}")



r = readability()
r.calculate_readability()

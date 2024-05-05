import re
import string
import random

from reserved_words import sql_reserved_words_upper
from tests.test_queries import longquery


import re
import random
import nltk
from nltk.corpus import words

class Anonymizer:
    def __init__(self, token_mode="random"):
        self.mapping = {}  # Dictionary from original tokens to sanitized tokens
        self.token_mode = token_mode  # random for random strings, dictionary for dictionary words
        if token_mode == "dictionary":
            # Load the English word list and shuffle it
            self.word_list = words.words()
            random.shuffle(self.word_list)

    def generate_random_string(self, length=8):
        if self.token_mode == "random":
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(length))
        elif self.token_mode == "dictionary":
            if not self.word_list:
                raise Exception("The word list has been exhausted.")
            return self.word_list.pop()  # Get a word and remove it from the list
        else:
            raise Exception(f"Unexpected token mode: {self.token_mode}")

    def anonymize(self, query):
        self.mapping = {}
        tokens = re.findall(r'\b\w+\b', query)
        for token in tokens:
            upper_token = token.upper()
            if upper_token not in sql_reserved_words_upper and re.match(r'\w+', token):
                if token not in self.mapping:
                    self.mapping[token] = self.generate_random_string()
                query = self.replace_in_string(token=token, replacement=self.mapping[token], string=query)
        return query

    def unanonymize(self, query):
        for original_token, sanitized_token in self.mapping.items():
            query = self.replace_in_string(token=sanitized_token, replacement=original_token, string=query)
        return query

    @staticmethod
    def replace_in_string(token, replacement, string):
        token = r"\b" + re.escape(token) + r"\b"
        modified_string = re.sub(token, replacement, string)
        return modified_string


def replace_in_string(token, replacement, string):
    token = r"\b" + token + r"\b"
    modified_string = re.sub(token, replacement, string)
    return modified_string






def test_quick(query):
    print("Original:")
    print(query)
    a = Anonymizer()
    res1 = a.anonymize(query)
    print("\nAnon:")
    print(res1)
    unres1 = a.unanonymize(res1)
    print("\nRestored:")
    print(unres1)

# test_quick("SELECT EmployeeID, LastName FROM Employees WHERE Department = 'Sales';")
test_quick(longquery)
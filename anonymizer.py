import json
import random
import re
import string

from reserved_words import sql_reserved_words_upper
from tests.test_queries import longquery


# TODO nltk required to .download('words') the first time, so might make sense to keep a local, gitted list of all words

# TODO how about anonymization of dates? right now we are treating-them as regular token, but that might confuse the LLM
#  a better way is to look at the list of tokens and convert dates to dates from other years

class Anonymizer:
    def __init__(self, token_mode="dictionary"):
        self.mapping = {}  # Dictionary from original tokens to sanitized tokens
        self.token_mode = token_mode  # random for random strings, dictionary for dictionary words
        if token_mode == "dictionary":
            # TODO remove innappropriate words
            with open('word_list.json', 'r') as f:
                self.word_list = json.load(f)
            random.shuffle(self.word_list)

    def generate_random_string(self, length=8):
        # TODO the list should be constantly refreshed in the background the avoid the cost of processing
        # TODO the random strings should have null intersection with: sql reserved words, and ideally original tokens

        # TODO can have "levels" of anonymization. For example, a table name as 'A' or common words like "data", "info"
        #  etc probably don't need to be anonymized
        if self.token_mode == "random":
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(length))
        elif self.token_mode == "dictionary":
            if not self.word_list:
                raise Exception("The word list has been exhausted.")
            return self.word_list.pop()
        else:
            raise Exception(f"Unexpected token mode: {self.token_mode}")

    def anonymize(self, query):
        self.mapping = {}
        # TODO need to consider that sql is NOT case sensitive, and therefore col1 and COL1 are the same thing!!
        tokens = re.findall(r'\b\w+\b', query)
        # TODO compare the performance of using tokens1 and parsing the list vs tokens2
        for token in tokens:
            upper_token = token.upper()
            if upper_token not in sql_reserved_words_upper and re.match(r'\w+', token):
                if token not in self.mapping:
                    self.mapping[token] = self.generate_random_string()
                # TODO there MUST be a more efficient way where we go through only once instead of <number of tokens>
                #  times, especially since we can hash the tokens and find they quickly. The only challenge is that as
                #  we go throught the query, we have to know where tokens start and end
                # TODO can always implement a string pattern algorithm directly in C/C++
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


def test_quick(query):
    print("Original:")
    print(query)
    a = Anonymizer(token_mode="random")
    a = Anonymizer(token_mode="dictionary")
    res1 = a.anonymize(query)
    print("\nAnon:")
    print(res1)
    unres1 = a.unanonymize(res1)
    print("\nRestored:")
    print(unres1)

# test_quick("SELECT EmployeeID, LastName FROM Employees WHERE Department = 'Sales';")
test_quick(longquery)
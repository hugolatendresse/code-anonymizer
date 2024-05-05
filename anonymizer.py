import re
import string
import random

from reserved_words import sql_reserved_words_upper
from tests.test_queries import longquery


class Anonymizer:

    def __init__(self, token_mode="random"):
        self.mapping = {} # Dictionary from original tokens to sanitize tokens
        self.token_mode = token_mode  # random for random strings, dictionary for dictionary words

    def generate_random_string(self, length=8):
        # TODO the list should be constantly refreshed in the background the avoid the cost of processing
        # TODO the random strings should have null intersection with: sql reserved words, and ideally original tokens

        # TODO can give the option between using dictionary words or random strings

        # TODO can have "levels" of anonymization. For example, a table name as 'A' or common words like "data", "info"
        #  etc probably don't need to be anonymized


        if self.token_mode == "random":
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(length))
        elif self.token_mode == "dictionary":
            # TODO even better here would be random words from the dictionary, without replacement
            # WRITE CODE HERE
            raise NotImplementedError
        else:
            raise Exception(f"unexpected token mode: {self.token_mode}")

    def anonymize(self, query):
        self.mapping = {}

        # TODO need to consider that sql is NOT case sensitive, and therefore col1 and COL1 are the same thing!!
        tokens = re.findall(r'\b\w+\b', query)
        # TODO compare the performance of using tokens1 and parsing the list vs tokens2
        # tokens1 = re.split(r"(\s+|,|;|\(|\))", query)
        for i, token in enumerate(tokens):
            if token.upper() not in sql_reserved_words_upper and re.match(r'\w+', token):
                if token not in self.mapping:
                    self.mapping[token] = self.generate_random_string()
                # TODO there MUST be a more efficient way where we go through only once instead of <number of tokens>
                #  times, especially since we can hash the tokens and find they quickly. The only challenge is that as
                #  we go throught the query, we have to know where tokens start and end
                # TODO can always implement a string pattern algorithm directly in C/C++
                query = replace_in_string(token=token, replacement=self.mapping[token], string=query)

        return query

    def unanonymize(self, query):
        for original_token, sanitized_token in self.mapping.items():
            query = replace_in_string(token=sanitized_token, replacement=original_token, string=query)
        return query


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
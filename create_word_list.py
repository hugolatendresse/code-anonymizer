import nltk
import json

nltk.download('words')
word_list = nltk.corpus.words.words()
with open('word_list.json', 'w') as f:
    json.dump(word_list, f)

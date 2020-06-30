#!/usr/bin/python3

import sys
import nltk
import string
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def str_preprocess(str):
    tokens = nltk.word_tokenize(str.lower())
    tokens = [re.sub(r'[^a-z]','',token) for token in tokens]
    tokens = [token for token in tokens if token]

    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]

    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(token, pos = 'v') for token in filtered_tokens]
    return lemmas

with open(sys.argv[1], 'r') as book_file:
    book = book_file.read()
if ('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">' in book):
    print('Book file is invalid.')
    sys.exit()
split_header = book.split('Title: ', 1)
split_title = split_header[1].split('\n\nAuthor: ', 1)
title = re.sub(r'\s+', ' ', split_title[0])
split_author = split_title[1].split('\n\nRelease Date: ', 1)
author = split_author[0]
split_date = split_author[1].split('\n\nLanguage: ', 1)
split_language = split_date[1].split('\n\nCharacter ', 1)
if not (split_language[0] == 'English'):
    print('Book language is not supported.')
    sys.exit()
split_begin = split_language[1].split('\n\n*** START OF THIS PROJECT GUTENBERG EBOOK', 1)
split_end = split_begin[1].split('End of the Project Gutenberg EBook', 1)

res = str_preprocess(split_end[0])
print(f'{title} by {author}')
print(res[:600])

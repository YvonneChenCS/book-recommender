#!/usr/bin/python3

import sys
import nltk
import string
import re

def str_preprocess(str):
    tokens = nltk.word_tokenize(str.lower())
    tokens = [re.sub(r'[^a-z]','',token) for token in tokens]
    tokens = [token for token in tokens if token]
    return tokens

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
print(f'{title} by {author}')
split_begin = split_author[1].split('\n\n*** START OF THIS PROJECT GUTENBERG EBOOK', 1)
split_end = split_begin[1].split('End of the Project Gutenberg EBook', 1)
res = str_preprocess(split_end[0])
print(res[:600])

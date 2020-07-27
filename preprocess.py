#!/usr/bin/python3

import os
import sys
import nltk
import string
import re
import glob
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds

def build_bookinfo():
    id_info = process_corpus_cache()[0]
    bookinfo = pd.DataFrame.from_dict(id_info).set_index('bookid')
    print(bookinfo)
    bookinfo.to_hdf('bookinfo.h5', key='bookinfo', mode='w')

def build_bookscores():
    id_corpus = process_corpus_cache()[1]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(list(id_corpus.values()))
    print("n_samples: %d, n_features: %d" % X.shape)
    U, s, Vh = svds(X, k = 3)
    print(f'U: {U.shape}, s: {s.shape}, Vh: {Vh.shape}')
    bookscores = pd.DataFrame(U, index=list(id_corpus.keys()))
    print('Bookscores: ')
    print(bookscores)
    bookscores.to_hdf('bookscores.h5', key='bookscores', mode='w')
    print('Eigenvalues: ')
    eigens = pd.DataFrame(s)
    print(eigens)
    eigens.to_hdf('bookscores.h5', key='eigens', mode='w')

def get_content(filename):
    bookid = filename.split('cache2/')[1].split('.')[0]
    with open(filename, 'r') as book_file:
        book = book_file.read()
    if ('!DOCTYPE' in book):
        print('Book file is invalid.')
        return '', '', ''
    split_header = book.split('Title: ', 1)
    split_title = split_header[1].split('\n\nAuthor: ', 1)
    title = re.sub(r'\s+', ' ', split_title[0])
    split_author = split_title[1].split('\n\n', 1)
    author = split_author[0]
    author = re.sub('\s+', ' ', author)
    split_date = split_author[1].split('\n\nLanguage: ', 1)
    split_language = split_date[1].split('\n\n', 1)
    if not (split_language[0] == 'English'):
        print('Book language is not supported.')
        return '', '', ''
    print(f'{title} by {author}')
    split_begin = split_language[1].split('*** START OF THIS PROJECT GUTENBERG EBOOK', 1)
    split_end = split_begin[1].split('*** END OF THIS PROJECT GUTENBERG EBOOK', 1)
    return title, author, split_end[0]

def str_preprocess(s):
    if (s == ''):
        return ''
    else:
        tokens = nltk.word_tokenize(s.lower())
        tokens = [re.sub(r'[^a-z]','',token) for token in tokens]
        tokens = [token for token in tokens if token]

        stop_words = set(stopwords.words('english'))
        filtered_tokens = [token for token in tokens if token not in stop_words]

        lemmatizer = WordNetLemmatizer()
        lemmas = [lemmatizer.lemmatize(token, pos = 'v') for token in filtered_tokens]
        return lemmas

def build_corpus_cache():
    os.makedirs('corpus', exist_ok=True)
    for filename in sorted(os.listdir('cache2')):
        print(f'Processing {filename}...')
        corpus_filename = f'/home/yvonne/books/corpus/corpus_{filename}'
        if not os.path.isfile(corpus_filename):
            title, author, content = get_content(f'/home/yvonne/books/cache2/{filename}')
            if content:
                res = str_preprocess(content)
                res = ' '.join(res)
                with open(corpus_filename, 'w+') as corpus_file:
                    print(title, file=corpus_file)
                    print(author, file=corpus_file)
                    corpus_file.write(res)

def process_corpus_cache():
    id_info = []
    #id_corpus = []
    id_corpus = {}
    for filename in sorted(os.listdir('corpus')):
        filename = f'/home/yvonne/books/corpus/{filename}'
        bookid = filename.split('/')[-1].split('.')[0].split('_')[1]
        with open(filename) as corpus_file:
            title = corpus_file.readline().rstrip()
            author = corpus_file.readline().rstrip()
            corpus = corpus_file.readline()
        id_info.append({
            'bookid' : bookid,
            'title' : title,
            'author' : author
        })
        id_corpus[bookid] = corpus
    return id_info, id_corpus

print('Creating corpus...')
build_corpus_cache()
print()
process_corpus_cache()
print('Building book info...')
build_bookinfo()
print()
print('Building book scores...')
build_bookscores()

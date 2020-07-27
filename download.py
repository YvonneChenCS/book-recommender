#!/usr/bin/python3

import requests
import os.path

def parse_index():
    start_found = False
    books = []
    for line in open('index.txt').readlines():
        line = line.strip()
        if not start_found and line.endswith('EBOOK NO.'):
            start_found = True
        elif start_found and len(line) == 78:
            line = line.split(' ')
            try:
                bookno = int(line[-1])
                title = ' '.join(line[:-1]).replace('\xa0', '').strip()
                books.append((bookno, title))
            except ValueError:
                pass
    return books 

def download_book(bookid):
    if not os.path.isfile(f'./cache/{bookid}.txt'):
        print(f'Writing {bookid}.txt')
        res = requests.get(f'http://www.gutenberg.org/files/{bookid}/{bookid}-0.txt')
        if ('!DOCTYPE' in res.text):
            print(f'Rewriting {bookid}.txt')
            res = requests.get(f'http://www.gutenberg.org/cache/epub/{bookid}/pg{bookid}.txt')
        open(f'./cache/{bookid}.txt', 'w').write(res.text)
        print(f'Written {bookid}.txt')

books = parse_index()[:1000]
for bookid, title in books:
    download_book(bookid)

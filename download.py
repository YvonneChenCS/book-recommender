#!/usr/bin/python3

import requests
import os.path
import pathlib

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
        elif start_found and len(line) == 79:
            line = line.split(' ')
            try:
                bookno = line[-1]
                bookno = int(bookno[:-1])
                title = ' '.join(line[:-1]).replace('\xa0', '').strip()
                books.append((bookno, title))
            except ValueError:
                pass
    return books

def download_book(bookid):
    current_dir = pathlib.Path('download.py').parent.absolute()
    if not os.path.isfile(f'{current_dir}/cache/{bookid}.txt'):
        print(f'Writing {bookid}.txt')
        res = requests.get(f'http://www.gutenberg.org/files/{bookid}/{bookid}-0.txt')
        if ('!DOCTYPE' in res.text):
            print(f'URL format error. Rewriting {bookid}.txt')
            res = requests.get(f'http://www.gutenberg.org/cache/epub/{bookid}/pg{bookid}.txt')
        open(f'{current_dir}/cache/{bookid}.txt', 'w').write(res.text)
        print(f'Written {bookid}.txt')

books = parse_index()
directory = "cache"
current_dir = pathlib.Path('download.py').parent.absolute()
path = os.path.join(current_dir, directory)
try:
    os.mkdir(path)
except FileExistsError:
    print('Cache directory already exists.')
for bookid, title in books:
   download_book(bookid)

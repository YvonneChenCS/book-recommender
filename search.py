#!/usr/bin/python3

import argparse
import pathlib
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def build_dict():
    title_id = {}
    current_dir = pathlib.Path('search.py').parent.absolute()
    df = pd.read_hdf(f'{current_dir}/bookinfo.h5')
    for index, row in df.iterrows():
        if row['title'] not in title_id:
            title_id[row['title']] = []
        title_id[row['title']].append(row.name)
    return title_id

def fuzzy_search(keyword, title_dict):
    current_dir = pathlib.Path('search.py').parent.absolute()
    bookinfo = pd.read_hdf(f'{current_dir}/bookinfo.h5')
    titles = bookinfo['title'].values
    title = process.extractOne(keyword, titles)
    title = title[0]
    search_bookinfo = {
        'bookid' : title_dict[title],
        'title' : title,
        'author' : bookinfo.loc[title_dict[title]]['author']
    }
    df = pd.DataFrame.from_dict(search_bookinfo).set_index('bookid')
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search book by [title].')
    parser.add_argument('title', metavar='title', help='book title')
    argv = parser.parse_args()
    title = argv.title
    id_dict = build_dict()
    search_bookinfo = fuzzy_search(title, id_dict)
    print(search_bookinfo)

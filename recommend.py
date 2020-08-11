#!/usr/bin/python3

import argparse
import pathlib
import pandas as pd
import numpy as np

def calculate_distances(bookid):
    def get_dist(row):
        diff = np.subtract(row.values, book.values)
        diff = np.square(diff)
        wts = eigens
        return np.sum(diff)

    current_dir = pathlib.Path('recommend.py').parent.absolute()
    bookscores = pd.read_hdf(f'{current_dir}/bookscores.h5').iloc[:,:100]
    eigens = pd.read_hdf(f'{current_dir}/eigens.h5').iloc[::-1].iloc[:100,0].values
    book = bookscores.loc[bookid]
    bookscores['dist'] = bookscores.apply(get_dist, axis=1)
    
    scores = bookscores.sort_values('dist')
    info = pd.read_hdf('bookinfo.h5')
    scores = scores.join(info)
    return scores

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recommend 5 closest books to [bookid].')
    parser.add_argument('bookid', metavar='bookid', help='bookid')
    argv = parser.parse_args()
    bookid = argv.bookid

    try:
        scores = calculate_distances(bookid)
    except KeyError:
        print('book not found')
        exit(1)

    print(scores[['dist', 'title', 'author']].head())

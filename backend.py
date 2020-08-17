import recommend
import search
from flask import Flask, request
app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend_books():
    bookid = request.form['bookid']
    scores = recommend.calculate_distances(bookid)
    scores = scores[['title', 'author']].head()
    print(scores)
    return scores.to_json(orient='records')

@app.route('/search', methods=['POST'])
def search_books():
    keyword = request.form['keyword']
    id_dict = search.build_dict()
    search_bookinfo = search.fuzzy_search(keyword, id_dict)
    print(search_bookinfo)
    return search_bookinfo.to_json(orient='records')

import recommend
import search
import json
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__, static_url_path='')
CORS(app)

@app.route('/', methods=['POST', 'GET'])
def recommend_books():
    keyword = request.form['keyword']
    def search_books():
        id_dict = search.build_dict()
        search_bookinfo = search.fuzzy_search(keyword, id_dict)
        return search_bookinfo.iloc[0].name
    bookid = search_books()
    scores = recommend.calculate_distances(bookid)
    scores = scores[['title', 'author']].head()
    scores['bookid'] = scores.index
    print(scores)
    return scores.to_json(orient='records')

@app.route('/gutenberg', methods=['POST', 'GET'])
def root():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


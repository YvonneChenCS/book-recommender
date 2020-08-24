import recommend
import search
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
#app.config['ENV'] = 'development'
#app.config['DEBUG'] = True
#app.config['TESTING'] = True
#app.logger.setLevel(logging.DEBUG)
CORS(app)

@app.route('/', methods=['POST'])
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

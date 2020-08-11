import recommend
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['POST'])
def recommend_books():
    bookid = request.form['bookid']
    scores = recommend.calculate_distances(bookid)
    scores = scores[['title', 'author']].head()
    print(scores)
    return scores.to_json(orient='records')

import requests
from flask import Flask, request, jsonify
from flask_jwt import jwt_required, current_identity

from shared.auth import jwt
from .db import db_client

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Bruce Wayne is Batman'
jwt.init_app(app)


@app.route('/reviews/<string:movie_id>')
def movie_reviews(movie_id):
    results = db_client.reviews.find({'movie_id': movie_id})
    reviews = []
    for result in results:
        reviews.append({
            'id': str(result['_id']),
            'user': result['user'],
            'movie_id': result['movie_id'],
            'comment': result['comment'],
            'rating': result['rating']
        })
    return jsonify(reviews)


@app.route('/reviews/<string:movie_id>', methods=['POST'])
@jwt_required()
def create_movie_review(movie_id):
    data = request.json
    # comprobamos si la peli existe
    url = f'http://localhost:5001/movies/{movie_id}'
    response = requests.get(url)
    if not response.ok:
        return jsonify({'error': 'Movie not found'}), 404
    review = {
        'user': current_identity['id'],  # cogemos el id del usuario del token
        'movie_id': movie_id,
        'comment': data['comment'],
        'rating': data['rating']
    }
    db_client.reviews.insert(review)  # deberíamos controlar que se guarda
    review['id'] = str(review['_id'])
    del review['_id']
    result = requests.post(url, json={'rating': data['rating']})
    return jsonify(review)

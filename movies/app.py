from flask import Flask, request, jsonify
from flask_jwt import jwt_required, current_identity

from shared.auth import jwt
from .db import db_client

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Bruce Wayne is Batman'
jwt.init_app(app)


@app.route('/movies/')
def movies_list():
    results = db_client.movies.find()
    movies = []
    for result in results:
        movies.append({
            'id': str(result['_id']),
            'title': result['title']  # mejor hacerlo así: result.get('title')
        })
    return jsonify(movies)

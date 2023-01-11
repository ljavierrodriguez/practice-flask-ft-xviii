import os
from datetime import datetime
from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, User
import sqlalchemy

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)
Migrate(app, db) # db init, db migrate, db upgrate
CORS(app)


@app.errorhandler(400)
def error_data(e):
    return jsonify(error=str(e)), 400

@app.route('/')
def main():
    return jsonify({ "message": "Welcome to Flask API" }), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200

@app.route('/api/users', methods=['POST'])
def insert_user():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        # active = request.json.get('active')
        # verified = request.json.get('verified')

        if not username:
            return jsonify({ "error": "username es requerido"}), 400

        if not password:
            return jsonify({ "error": "password es requerido"}), 400

        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({ "error": "username ya existe"}), 400

        user = User()
        user.username = username
        user.password = password
        user.save()

        # db.session.add(user)
        # db.session.commit()

        return jsonify(user.serialize()), 201
    except:
        abort(400, "Error al crear un usuario")


@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    
    username = request.json.get('username')
    password = request.json.get('password')
    # active = request.json.get('active')
    # verified = request.json.get('verified')

    user = User.query.get(id)
    user.username = username
    user.password = password
    user.updated_at = datetime.now()
    user.update()

    # db.session.commit()

    return jsonify(user.serialize()), 200

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    pass



if __name__ == '__main__':
    app.run()
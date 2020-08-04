import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity

from resources.user import UserRegister
from resources.story import Story

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '123456'
api = Api(app)

# Endpoints
jwt = JWT(app, authenticate, identity)  # /auth
api.add_resource(UserRegister, '/register')
api.add_resource(Story, '/blog/<string:username>')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5002, debug=True)

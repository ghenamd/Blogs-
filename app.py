from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity

from resources.user import UserRegister
from resources.story import Story

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '123456'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth


@app.before_request
def create_tables():
    db.create_all()


api.add_resource(UserRegister, '/register')
api.add_resource(Story, '/blog/<string:username>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5002, debug=True)

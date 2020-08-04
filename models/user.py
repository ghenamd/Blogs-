from db import db
from models.story import StoryModel


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

    stories = db.relationship('StoryModel', lazy='dynamic')

    def json(self):
        return {'username': self.username, 'stories': [story.json() for story in self.stories.all()]}

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_user_by_name(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

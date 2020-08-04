from db import db


class StoryModel(db.Model):
    __tablename__ = 'story'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    title = db.Column(db.String(50))
    text = db.Column(db.String(500))
    image = db.Column(db.String)
    parent_username = db.Column(db.Integer, db.ForeignKey('users.username'))

    stories = db.relationship('UserModel')

    def __init__(self, date, title, text, image, parent_username):
        self.date = date
        self.title = title
        self.text = text
        self.image = image
        self.parent_username = parent_username

    @classmethod
    def find_stories_by_username(cls, username):
        return StoryModel.query.filter_by(parent_username=username).all()

    @classmethod
    def find_story_by_title(cls, title):
        return StoryModel.query.filter_by(title=title).first()

    def json(self):
        return {'date': self.date, 'title': self.title, 'text': self.text, 'image': self.image}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

from db import db


class StoryModel(db.Model):
    __tablename__ = 'story'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    title = db.Column(db.String(50))
    text = db.Column(db.String(500))
    image = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('UserModel')

    def __init__(self, date, title, text, image, user_id):
        self.date = date
        self.title = title
        self.text = text
        self.image = image
        self.user_id = user_id

    @classmethod
    def find_stories_by_user_id(cls, user_id):
        return StoryModel.query.filter_by(user_id=user_id).all()

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

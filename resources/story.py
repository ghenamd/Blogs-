from flask_restful import Resource, reqparse
from models.story import StoryModel
from models.user import UserModel
from flask_jwt import jwt_required


class Story(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'date',
        type=str,
        required=True
    )

    parser.add_argument(
        'title',
        type=str,
        required=True,
        help="Each story needs a title"
    )

    parser.add_argument(
        'text',
        type=str,
        required=True,
        help="Each story needs a text"
    )

    parser.add_argument(
        'image',
        type=str
    )

    def get(self, user_id):

        stories = StoryModel.find_stories_by_user_id(user_id)
        user_name = UserModel.find_user_by_id(user_id)

        if stories:
            return {'user_id': user_id, 'story': [story.json() for story in stories]}
        else:
            return {'message': "There are no stories for username'{}' ".format(user_name),
                    'error': 404}, 404  # Not found

    @jwt_required()
    def post(self, username):

        user = UserModel.find_user_by_name(username)
        if not user:
            return {'message': "A user with name '{}' doesn't exists".format(
                username),
                       'error': 400}, 400  # bad request

        data = Story.parser.parse_args()

        blog_title = StoryModel.find_story_by_title(data['title'])
        if blog_title:
            return {'message': "A story with the title '{}' already exists".format(data['title']),
                    'error': 400}, 400

        story = StoryModel(data['date'], data['title'], data['text'], data['image'], username)

        try:
            story.save_to_db()
        except:
            return {'message': 'An error occurred while inserting a new story',
                    'error': 500}, 500  # Internal server error

        return {'message': 'A new story has been added successfully',
                'error': 201}, 201  # created

    @jwt_required()
    def delete(self, user_id):
        stories = StoryModel.find_stories_by_user_id(user_id)
        user_name = UserModel.find_user_by_id(user_id)

        if not stories:
            return {"message": "This User's blog is empty'"}
        else:
            try:
                for story in stories:
                    story.delete_from_db()
            except:
                return {'message': "An error occurred while deleting blog",
                        'error': 400}

        return {'message': "'{}' blog has been deleted successfully ".format(user_name),
                'error': 200}

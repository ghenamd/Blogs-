from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank"
    )

    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_user_by_name(data['username']):
            return {'message': "A User with name: '{}' already exists".format(data['username']),
                    'error': 400}, 400
        else:
            user = UserModel(username=data['username'],
                             password=data['password'])
            user.save_to_db()
            return {'message': "User with name '{}'created successfully".format(data['username']),
                    'error': 201}, 201

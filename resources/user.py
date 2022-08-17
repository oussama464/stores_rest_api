from dataclasses import dataclass
from utils.db_utilities import SQLite
from flask_restful import Resource, reqparse
from models.user import UserModel
import pathlib

DB_PATH = pathlib.Path(__file__).parent.parent.joinpath("data.db")


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="username cannot be left blank"
    )
    parser.add_argument(
        "password", type=str, required=True, help="cannot be left blank"
    )

    def post(self):
        user_data = UserRegister.parser.parse_args()
        username, user_password = user_data["username"], user_data["password"]
        if UserModel.find_by_username(username):
            return {
                "message": f"user {username} already registred in db"
            }, 400  # bad request
        user = UserModel(username, user_password)
        user.save_to_db()
        return {"message": f"user {username} registred sucessfully !!"}, 201

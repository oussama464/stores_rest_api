import os
import re
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


from security import authenticate, identifty
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from utils.db_utilities import db


# or other relevant config var
uri = os.getenv("DATABASE_URL", "sqlite:///data.db")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "oussama"
api = Api(app)  # add resources (classes) to api


db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identifty)


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

if __name__ == "__main__":

    app.run(port=5000, debug=True)

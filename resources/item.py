from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="cannot be left blank")
    parser.add_argument(
        "store_id", type=int, required=True, help="Evry item needs a store id"
    )

    @jwt_required()
    def get(self, name):

        # item = next(filter(lambda x: x["name"] == name, items), None)
        result = ItemModel.find_by_name(name)

        return {"item": result}, 200 if result else 404

    def post(self, name):
        result = ItemModel.find_by_name(name)

        if result:
            return {"message": f"item {name} already exists"}, 400  # bad request

        request_data = self.parser.parse_args()
        item = ItemModel(name, request_data["price"], request_data["store_id"])
        item.save_to_db()
        return item.json(), 201  # 201 is for created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db(self)
        return {"message": f"item {name} deleted"}

    def put(self, name):
        request_data = self.parser.parse_args()
        item = ItemModel(name, request_data["price"], request_data["store_id"])
        item.save_to_db()

        return item.json(), 201


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}

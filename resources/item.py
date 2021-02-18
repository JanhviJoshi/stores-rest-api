from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    # we want to make sure that our json payload (which is the data that the client sends to us
    # while making a put request) is correct and has the fields that we desire (in this case, the field
    # 'price')
    # thus we use the parser
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")  # we only added the argument 'price' here so if any other field is given by client when making the request,
                                                                 # it will be ignored

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id")


    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "An error occurred while inserting item"}, 500

        if item:
            return item.json()
        return {"message": "item not found"}, 404

    def post(self, name):  # post method should have the exact same signature as the get method

        # our app does not allow duplication of name of items, that is why below piece of codes
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400  # 400 bcs asking to create a new resource that already exists is a bad request

        # using parser below:
        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting item"}, 500  # 500 means internal server error and is usually given to indicate to the user that they are not at fault

        return item.json(), 201  # to let our client know that our method worked

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        # allowing the 'price' data into our codes, and also that it should be of type float and is reqd
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            # item doesnt exist already
            item = ItemModel(name, data['price'], data['store_id'])
            try:
                item.insert()
            except:
                return {"message": "An error occurred while inserting item"}, 500
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}  # return list of items

import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity

from resources.user import UserRegister
from resources.item import ItemList, Item
from resources.store import Store, StoreList

from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'  # this key needs to more complicated and secure
api = Api(app)  # makes it easier for us to define what CRUD operations can be defined for each resource of our api

jwt = JWT(app, authenticate, identity)  # creates a new endpoint => /auth


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')  # instead of writing the @app.route(...) we are doing this
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')  # when we hit the endpoint /register, the UserRegister class ka post method is called


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)  # default value is also 5000, debug param shows good error messages

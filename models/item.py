from codes.db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))  # means the id value of stores table is the foreign key of this table
    # this way, we know each item belongs to which store and that a particular store has which items
    store = db.relationship('StoreModel')  # every item has another property called store which matches the store_id

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        # connection = sqlite3.connect('./data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):  # updates and/or inserts data
        db.session.add(self)  # a collection of objects that we will add to the db, in this case, we are only adding 1
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
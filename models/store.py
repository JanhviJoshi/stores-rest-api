from codes.db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # back reference
    # allows to see which items belong to the store of a given id
    items = db.relationship('ItemModel', lazy='dynamic')  # items is a list

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):  # updates and/or inserts data
        db.session.add(self)  # a collection of objects that we will add to the db, in this case, we are only adding 1
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
from codes.db import db


# our api cannot receive data into this class and send the class as
# json representation. It is a helper.
class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):  # username_mapping
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):  # userid_mapping
        return cls.query.filter_by(id=_id).first()
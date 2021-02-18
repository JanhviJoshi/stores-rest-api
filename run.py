from app import app
from db import db

db.init_app(app)


@app.before_first_request  # runs the method that it decorates before the 1st request to our app
def create_tables():
    db.create_all()
    print("inside create_tables")
    # Because our models are imported and they define __tablename__ and the columns,
    # db.create_all knows what tables and columns to create
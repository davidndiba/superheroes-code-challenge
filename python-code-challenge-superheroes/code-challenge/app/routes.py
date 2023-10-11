from app import app

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
# Create a database table for the users.  This is done by creating an object that inherits from db.Model and then defining colum

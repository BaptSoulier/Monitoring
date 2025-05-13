from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    """Initialize the MongoDB connection with the Flask application."""
    mongo.init_app(app)

def get_db():
    """Return the MongoDB database object."""
    return mongo.db

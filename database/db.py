from flask_pymongo import PyMongo

mongo = PyMongo()  # Initialisez PyMongo ici

def init_db(app):
    """Initialise la connexion à MongoDB avec l'application Flask."""
    mongo.init_app(app)  # Associez PyMongo à l'application Flask
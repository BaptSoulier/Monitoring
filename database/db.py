from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    """Initialise la connexion à MongoDB avec l'application Flask."""
    mongo.init_app(app)

def get_db():
    """Retourne l'objet base de données MongoDB."""
    return mongo.db

from flask import Flask
from config import app_config
import logging
from core.file_watcher import run_watcher_in_thread, load_watched_files
from core.log_manager import setup_logging
from flask_pymongo import PyMongo  # Importez PyMongo ici explicitement

mongo = PyMongo() #Instanciation de pymongo

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config.app_config[config_name])

    setup_logging()
    # Initialisez PyMongo ici, après avoir créé l'application Flask
    try:
        mongo.init_app(app)
        print("PyMongo initialized successfully!")  # Ajout d'un message de confirmation
    except Exception as e:
        print(f"Error initializing PyMongo: {e}")  # Ajout d'un message d'erreur détaillé

    from webapp import routes
    app.register_blueprint(routes.main_bp)

    watched_files = load_watched_files()
    if watched_files:
        run_watcher_in_thread(watched_files, watched_files)

    return app

app = create_app(config_name="development")

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])

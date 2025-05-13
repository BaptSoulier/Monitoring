from flask import Flask
from config import app_config
from flask_pymongo import PyMongo
import logging
from core.file_watcher import run_watcher_in_thread, load_watched_files
from core.log_manager import setup_logging

mongo = PyMongo()

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(app_config.app_config[config_name])
    
    # Initialize logging
    setup_logging()
    
    # Initialize PyMongo *after* configuration
    mongo.init_app(app)
    
    from webapp import routes
    app.register_blueprint(routes.main_bp)
    
    # Start the file watcher thread
    watched_files = load_watched_files()
    if watched_files:
        run_watcher_in_thread(watched_files, watched_files)
    
    return app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
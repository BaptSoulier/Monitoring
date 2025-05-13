import logging
from config.app_config import Config
from datetime import datetime
from flask import current_app, g

def setup_logging():
    logging.basicConfig(filename=Config.LOG_FILE, level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def get_mongo():
    """Obtient la connexion MongoDB à partir de l'objet global g."""
    if 'mongo' not in g:
        g.mongo = current_app.extensions['pymongo'].db
    return g.mongo

def log_to_db(level, message, file_path=None):
    timestamp = datetime.now()
    log_entry = {
        'timestamp': timestamp,
        'level': level,
        'message': message,
        'file_path': file_path
    }
    try:
        mongo = get_mongo() # Utilisez la connexion globale
        mongo.logs.insert_one(log_entry)  # Utilisez la collection 'logs'
    except Exception as e:
        logging.error(f"Erreur lors de l'insertion du log dans MongoDB : {e}", exc_info=True)

def log_info(message, file_path=None):
    log_to_db('INFO', message, file_path)

def log_warning(message, file_path=None):
    log_to_db('WARNING', message, file_path)

def log_error(message, file_path=None, exc_info=False):
    log_to_db('ERROR', message, file_path)
    if exc_info:
        logging.exception(message)

if __name__ == '__main__':
    setup_logging()
    from webapp import app
    with app.app_context():
        # Pas besoin d'init_db ici, PyMongo s'en charge
        log_info("This is an info message.", "test.py")
        log_warning("This is a warning message.", "test.py")
        try:
            1 / 0
        except Exception as e:
            log_error("This is an error message.", "test.py", exc_info=True)

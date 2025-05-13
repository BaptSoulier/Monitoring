import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cle_secrete_tres_difficile'
    LOG_FILE = 'logs/app.log'
    WATCHED_FILES_FILE = 'config/watched_files.json'
    DEBUG = True
    
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/moniteur_systeme'  # URI de connexion MongoDB
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME') or 'moniteur_systeme' # Nom de la base de données

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

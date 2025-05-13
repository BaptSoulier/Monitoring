import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    LOG_FILE = 'logs/app.log'
    WATCHED_FILES_FILE = 'config/watched_files.json'
    DEBUG = True

    # MongoDB Configuration
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/moniteur_systeme'
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME') or 'moniteur_systeme'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
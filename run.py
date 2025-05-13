from webapp import app
from database.db import init_db  

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
#from app import create_app
from app import app
from app.database import init_db
from time import sleep


if __name__ == "__main__":    
    #app = create_app()
    #init_db()
    app.run()
    
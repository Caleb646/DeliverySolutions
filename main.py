#from app import create_app
from app import app
from app.database import init_db, StorageOps
from time import sleep


if __name__ == "__main__":    
    #app = create_app()
    #init_db()
    #StorageOps.calculate_storage_fees()
    app.run()
    
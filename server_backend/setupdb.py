from wombats_db import Wombats_Db
from scrape_locations import db_setup

if(db_manager.is_empty()):
    db = db_setup()
    db.setup_database()
    return "Successful"
else:
    return "DB already exists"
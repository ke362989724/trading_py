
from .database import Database


database = Database()
db = database.db
bulk_insert = database.bulk_insert
insert_one = database.insert_one
find_all = database.find_all
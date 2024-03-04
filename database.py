import pymongo

from config import settings

client = pymongo.MongoClient(settings.database_url)
db = client.staff
collection = db.salary


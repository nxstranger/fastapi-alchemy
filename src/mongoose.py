import urllib.parse
from pymongo import MongoClient
from .settings import settings

MONGODB_USER = settings.MONGODB_USER
MONGODB_PASSWORD = settings.MONGODB_PASSWORD
MONGODB_HOST = settings.MONGODB_HOST
MONGODB_PORT = settings.MONGODB_PORT

client = MongoClient(
    'mongodb://{0}:{1}@{2}:{3}'.format(
        MONGODB_USER,
        urllib.parse.quote_plus(MONGODB_PASSWORD),
        MONGODB_HOST,
        MONGODB_PORT
    ),
)


adv_db = client['temp_db']
adv_collection = adv_db["adverts"]


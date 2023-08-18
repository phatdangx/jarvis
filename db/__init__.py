from pymongo import MongoClient
from utils.constants import *


client = MongoClient(MONGO_SERVER, serverSelectionTimeoutMS=1000, connectTimeoutMS=10000)
db = client["{}".format(MONGO_DATABASE)]
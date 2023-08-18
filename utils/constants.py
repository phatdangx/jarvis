from config import Config

TOKEN = Config["jarvis"]["token"]

ADMIN_CONTACT = "@{}".format(Config["admin"])

MONGO_SERVER = Config["mongodb"]["host"]
MONGO_DATABASE = Config["mongodb"]["database"]
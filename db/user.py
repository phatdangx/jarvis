from utils import logger

import db
import time


def find_user_by_telegram_id(id):
    user = db.user.find_one({"telegram_id": str(id)})


def insert_new_user(data):
    try:
        data["create_time"] = time.time()
        r = db.user.insert_one(data)
        return True
    except Exception as e:
        logger.error("insert new user %s".format(str(e)))
        return False

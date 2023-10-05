from utils import logger
from db import db

import time


def find_user_by_telegram_id(id):
    user = db.user.find_one({"telegram_id": id})
    return user


def find_user_by_username(username):
    user = db.user.find_one({"username":username})
    return user

def find_user_by_employee_id(id):
    user = db.user.find_one({"employee_id": id})
    return user


def insert_new_user(data):
    try:
        data["create_time"] = time.time()
        _ = db.user.insert_one(data)
        return True
    except Exception as e:
        logger.error("insert new user {}".format(str(e)))
        return False


def remove_user_by_employee_id(id):
    try:
        r = db.user.delete_one({"employee_id": str(id)})
        return True
    except Exception as e:
        logger.error("delete user error {}".format(str(e)))
        return False


def update_user(filter, updates):
    try:
        r = db.user.update_one(
            filter=filter,
            update={
                "$set": updates
            }
        )
        if r.matched_count == 1:
            return True
        return False
    except Exception as e:
        logger.error("update user error {}".format(str(e)))
        return False
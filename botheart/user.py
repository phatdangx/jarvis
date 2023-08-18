# -*- coding: utf-8 -*-
"""
    Provides the Jarvis User class.
"""
from botheart import dblog, dblogr, redis_client, redis_key_pattern

import json


class User(object):
    """Represents a telegram user.

        Args:
            name (str): The user's unique telegram username.
            user_id (str): The user's unique telegram id.
            group (Optional[str]): The user's group.
    """

    def __init__(self, name, user_id, group=None, employee_id=None):
        self.__name = name
        self.__id = user_id
        self.__group = group
        self.__employee_id = employee_id

    def has_access(self, groups):
        """Checks if the user is in given group.

            Returns True if given user has access rights
            to the given group.

            Args:
                groups (list): The group's name.

            Returns:
                bool: True if user is in the given group, otherwise False.
        """
        if self.__id:
            user = redis_client.get(redis_key_pattern.format(self.__id))
            if not user:
                user = dblogr.jarvis_user.find_one({"telegram_id": str(self.__id)})
                if not user:
                    return False
                del user["_id"]
                redis_client.set(redis_key_pattern.format(self.__id), json.dumps(user))
            else:
                user = json.loads(user)
            is_in_groups = True if user["group"] in groups else False
            is_admin = True if "role" in user and user["role"] == "admin" else False
            is_mod = True if "role" in user and user["role"] == "mod" else False
            return is_in_groups or is_admin or is_mod
        return False

    def has_been_added(self):
        """Checks if the user is first access to the bot

            Returns:
                bool: True if user is in the given group, otherwise False.
        """
        if self.__id:
            user = redis_client.get(redis_key_pattern.format(self.__id))
            if user is not None:
                return True
        user = dblogr.jarvis_user.find_one(
            {
                "employee_id": self.__employee_id,
            }
        )
        if user is not None:
            return True
        return False

    def verify_secret_code(self, code):
        user = dblogr.jarvis_user.find_one(
            {
                "employee_id": self.__employee_id,
            }
        )
        if user and "secret" in user and user["secret"] == code:
            dblog.jarvis_user.update_one(
                {
                    "employee_id": self.__employee_id,
                    "secret": code
                },
                {
                    "$set": {
                        "telegram_id": str(self.__id),
                        "is_active": True,
                    }
                }
            )
            return True
        return False

    def require_admin(self):
        if self.__id:
            user = redis_client.get(redis_key_pattern.format(self.__id))
            if not user:
                user = dblogr.jarvis_user.find_one({"telegram_id": str(self.__id)})
                if not user:
                    return False
                del user["_id"]
                redis_client.set(redis_key_pattern.format(self.__id), json.dumps(user))
            else:
                user = json.loads(user)
            is_admin = True if user["role"] == "admin" else False
            return is_admin
        return False

    def require_group_mod(self, groups):
        if self.__id:
            user = redis_client.get(redis_key_pattern.format(self.__id))
            if not user:
                user = dblogr.jarvis_user.find_one({"telegram_id": str(self.__id)})
                if not user:
                    return False
                del user["_id"]
                redis_client.set(redis_key_pattern.format(self.__id), json.dumps(user))
            else:
                user = json.loads(user)
            is_group_mod = True if user["role"] == "mod" and user["group"] in groups else False
            return is_group_mod
        return False

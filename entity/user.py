# -*- coding: utf-8 -*-
"""
    Provides the Jarvis User class.
"""
from db.user import *

class User(object):
    """Represents a telegram user.

        Args:
            name (str): The user's unique telegram username.
            user_id (str): The user's unique telegram id.
            group (Optional[str]): The user's group.
    """

    def __init__(self, username, telegramid, group=None, employee_id=None):
        self.__username = username
        self.__telegramid = telegramid
        self.__group = group
        self.__employee_id = employee_id

    def has_access(self, groups):
        """
            Checks if the user is in given group.
            Returns True if given user has access rights
            to the given group.

            Args:
                groups (list): The group's name.

            Returns:
                bool: True if user is in the given group, otherwise False.
        """
        if self.__telegramid:
            user = find_user_by_telegram_id(self.__telegramid)
            if not user:
                return False
            is_in_groups = True if user["group"] in groups else False
            is_admin = True if "role" in user and user["role"] == "admin" else False
            is_mod = True if "role" in user and user["role"] == "mod" else False
            return is_in_groups or is_admin or is_mod
        return False

    def has_been_added(self):
        """
            Checks if the user is first access to the bot
            Returns:
                bool: True if user is in database, otherwise False
        """
        user = find_user_by_username(self.__username)
        if user is None:
            return False
        return True

    def require_admin(self):
        """
            Checks if the user is admin by checking field role in database
            Returns:
                bool: True if user is admin, otherwise False
        """
        if self.__telegramid:
            user = find_user_by_telegram_id(self.__telegramid)
            if not user:
                return False
            is_admin = True if user["role"] == "admin" else False
            return is_admin
        return False

    def require_group_mod(self, groups):
        """
            Checks if the user is moderator by checking field role in database
            Returns:
                bool: True if user is moderator, otherwise False
        """
        if self.__telegramid:
            user = find_user_by_telegram_id(self.__telegramid)
            if not user:
                return False
            is_group_mod = True if user["role"] == "mod" and user["group"] in groups else False
            return is_group_mod
        return False

    def update_user_telegram_id(self) -> None:
        """
            Update telegram id after user first interaction with the bot
        """
        if self.__telegramid:
            r = update_user(
                {
                    "username": self.__username
                },
                {
                    "telegram_id": self.__telegramid
                }
            )
            if not r:
                logger.error('fail to log telegram id of user {}'.format(self.__username))

    def get_user_group(self):
        """
            Return user group
        """
        if self.__telegramid:
            user = find_user_by_telegram_id(self.__telegramid)
            return user["group"] if "group" in user else ""
        return ""

    def insert_mongo(self, role):
        user = {
            "username": self.__username,
            "telegram_id": self.__telegramid,
            "role": role,
            "group": self.__group,
            "employee_id": self.__employee_id
        }
        insert_new_user(user)
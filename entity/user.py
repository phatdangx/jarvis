# -*- coding: utf-8 -*-
"""
    Provides the Jarvis User class.
"""
from botheart import dblog, dblogr, redis_client, redis_key_pattern
from db.user import *

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
        """
            Checks if the user is in given group.
            Returns True if given user has access rights
            to the given group.

            Args:
                groups (list): The group's name.

            Returns:
                bool: True if user is in the given group, otherwise False.
        """
        if self.__id:
            user = find_user_by_telegram_id(self.__id)
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
        user = find_user_by_telegram_id(self.__id)
        if user is None:
            return False
        return True

    def require_admin(self):
        """
            Checks if the user is admin by checking field role in database
            Returns:
                bool: True if user is admin, otherwise False
        """
        if self.__id:
            user = find_user_by_telegram_id(self.__id)
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
        if self.__id:
            user = find_user_by_telegram_id(self.__id)
            if not user:
                return False
            is_group_mod = True if user["role"] == "mod" and user["group"] in groups else False
            return is_group_mod
        return False

# -*- coding: utf-8 -*-
"""
    Provides decorator functions for user authentication.
"""
from utils.constants import SUPER_ADMIN_CONTACT
from entity.user import User


def requires_user_group(*decorator_args):
    """Checks if the user has access to the decorated function.

        Checks if the user who sent the message is in the given
        user group thus has access to the decorated function.

        Args:
            group(str): The group's name.

        Returns:
            func: The decorator function.
    """

    def decorate(func):
        def call(*args, **kwargs):
            update = args[0]
            context = args[1]

            username = update.message.from_user.name
            user_id = update.message.from_user.id
            user = User(username, user_id)
            required_groups = list(decorator_args)

            # Check if user has required group
            has_access = user.has_access(required_groups)

            if not has_access:
                context.bot.sendMessage(
                    chat_id=update.message.chat_id,
                    text="⛔️ Contact {} to review your permission".format(SUPER_ADMIN_CONTACT),
                    reply_to_message_id=update.message.message_id
                )
                return

            result = func(*args, **kwargs)
            return result

        return call

    return decorate


def verify_user_init():
    """Verify if user is allowed to use the bot
        Returns:
            func: The decorator function.
    """
    def decorate(func):
        def call(*args, **kwargs):
            update = args[0]
            context = args[1]

            bot = context.bot

            username = update.message.from_user.name
            user_id = update.message.from_user.id
            user = User(
                name=username,
                user_id=user_id,
            )
            
            # Check if user is allowed to use bot
            print(username)
            print(user.has_been_added())
            is_allowed = user.has_been_added() or username == SUPER_ADMIN_CONTACT
            if not is_allowed:
                bot.sendMessage(
                    chat_id=update.message.chat_id,
                    text="⛔️ Contact {} to set permission for you".format(SUPER_ADMIN_CONTACT),
                    reply_to_message_id=update.message.message_id
                )
                return

            # Log telegram_id to database
            user.update_user_telegram_id()

            result = func(*args, **kwargs)

            return result

        return call

    return decorate


def requires_admin():
    """Checks if the user has access to the decorated function.

        Checks if the user who sent the message is in the given
        user group thus has access to the decorated function.

        Args:
            group(str): The group's name.

        Returns:
            func: The decorator function.
    """

    def decorate(func):
        def call(*args, **kwargs):
            update = args[0]
            context = args[1]

            username = update.message.from_user.name
            user_id = update.message.from_user.id
            user = User(username, user_id)

            # Check if user is admin
            is_admin = user.require_admin()

            if not is_admin:
                context.bot.sendMessage(
                    chat_id=update.message.chat_id,
                    text="⛔️ You are not allowed to run this command ⛔️",
                    reply_to_message_id=update.message.message_id
                )
                return

            result = func(*args, **kwargs)
            return result

        return call

    return decorate


def requires_group_mod(*decorator_args):
    """Checks if the user has access to the decorated function.

        Checks if the user who sent the message is in the given
        user group thus has access to the decorated function.

        Args:
            group(str): The group's name.

        Returns:
            func: The decorator function.
    """

    def decorate(func):
        def call(*args, **kwargs):
            update = args[0]
            context = args[1]

            username = update.message.from_user.name
            user_id = update.message.from_user.id
            user = User(username, user_id)
            required_group = list(decorator_args)

            # Check if user is mod of a group
            is_mod = user.require_group_mod(required_group)

            if not is_mod:
                context.bot.sendMessage(
                    chat_id=update.message.chat_id,
                    text="⛔️ You are not allowed to run this command ⛔️",
                    reply_to_message_id=update.message.message_id
                )
                return

            result = func(*args, **kwargs)
            return result

        return call

    return decorate

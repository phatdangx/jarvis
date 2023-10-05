from telegram.ext import CommandHandler
from telegram.parsemode import ParseMode
from utils.decorator import *

from business.admin import *

class AdminCommand(object):
    """
        Provides user command handlers for admin
    """

    def __init__(self, dispatcher):
        self.__dispatcher = dispatcher
        self.__register_handlers()

    def __register_handlers(self):
        """
            Registers the admin commands.
        """
        self.__dispatcher.add_handler(CommandHandler("help", self.__admin_help))
        self.__dispatcher.add_handler(CommandHandler("adduser", self.__add_user, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("rmu", self.__rm_user, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("viewuser", self.__viewuser, pass_args=True))

    @staticmethod
    @requires_admin()
    def __admin_help(update, context):
        """Command handler function for `adminhelp` command.

            Sends a list of all available commands to the
            client.

            Args:
                bot (telegram.Bot): The bot object.
                update (telegram.Update): The sent update.
        """

        template = "*{command_order}\.{command_help}* :\n \- Syntax: `{command_synctax}`\n \- Example: `{command_ex}`\n\n"
        help_dictionary = {
            "adduser": template.format(
                command_order=1,
                command_help="Add user",
                command_synctax="/adduser <username> <employee_id> <group>",
                command_ex="/adduser johndoe 150789 hr"
            ),
            "rmu": template.format(
                command_order=2,
                command_help="Remove user",
                command_synctax="/rmu <employee_id>",
                command_ex="/rmu 150789"
            ),
            "viewuser": template.format(
                command_order=3,
                command_help="View user detail",
                command_synctax="/viewuser <employee_id>",
                command_ex="/viewuser 150789"
            )
        }
        message = "*JARVIS ADMIN COMMANDS*:\n\n"
        for key in help_dictionary.keys():
            message += help_dictionary[key]
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_admin()
    def __add_user(update, context):
        """Command handler function for `adduser` command.

            Adds a telegram user to a user group.

            Args:
                update (telegram.Update): The sent update.
                context (telegram.Context): The context
        """
        args = context.args
        bot = context.bot
        if len(args) != 3:
            message = "Usage: <username> <employee id> <group>"
            bot.sendMessage(
                chat_id=update.message.chat_id,
                text=message,
                reply_to_message_id=update.message.message_id
            )
            return
        new_user = {
            "username": args[0],
            "employee_id": args[1],
            "group": args[2].lower(),
            "role": "user"
        }
        message = add_new_user(new_user)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_admin()
    def __rm_user(update, context):
        """Command handler function for `rmuser` command.

            Removes a telegram user from a usergroup.

            Args:
                bot (telegram.Bot): The bot object.
                update (telegram.Update): The sent update.
                args (list): The command's arguments.
        """
        bot = context.bot
        args = context.args
        if len(args) != 1:
            message = "Usage: rmu <employee id>"
            bot.sendMessage(chat_id=update.message.chat_id, text=message)
            return

        message = remove_user_by_employee_id(args[0])

        bot.sendMessage(
            chat_id=update.message.chat_id, 
            text=message,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_admin()
    def __viewuser(update, context):
        """Command handler to view user detail
        """
        bot = context.bot
        args = context.args
        if len(args) != 1:
            message = "Usage: viewuser <employee id>"
            bot.sendMessage(chat_id=update.message.chat_id, text=message)
            return

        message = viewuser(args[0])

        bot.sendMessage(
            chat_id=update.message.chat_id, 
            text=message,
            reply_to_message_id=update.message.message_id
        )
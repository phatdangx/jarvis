from telegram.ext import CommandHandler
from telegram.parsemode import ParseMode
from utils.decorator import *

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
        self.__dispatcher.add_handler(CommandHandler("adhelp", self.__admin_help))
        self.__dispatcher.add_handler(CommandHandler("adduser", self.__add_user, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("rmu", self.__rm_user, pass_args=True))

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
                command_synctax="/adduser <employee_id> <email> <group>",
                command_ex="/adduser 1507890 user@company.com sample_tele_username hr"
            ),
            "rmu": template.format(
                command_order=2,
                command_help="Remove user",
                command_synctax="/rmu ",
                command_ex="/rmu 1507890"
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
            message = "Usage: <employee_id> <aha_email> <group>"
            bot.sendMessage(
                chat_id=update.message.chat_id,
                text=message,
                reply_to_message_id=update.message.message_id
            )
            return
        employee_id = args[0]
        email = args[1]
        group = args[2]
        secret = generate_secret()
        access_code = str(secret) + str(employee_id)
        new_jarvis_user = {
            "employee_id": employee_id,
            "email": email,
            "group": group.upper(),
            "secret": secret
        }
        dblog.jarvis_user.insert_one(new_jarvis_user)
        send_email(
            subject="{} - Jarvis Bot Activation".format(config["env"].upper()),
            body=ACTIVATION_EMAIL.format(
                bot_user_name=config["jarvis"]["user_name"],
                secret=access_code
            ),
            to_addresses=[email]
        )
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Add {} successfully".format(employee_id),
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
        if len(args) != 2:
            message = "Usage: rmuser <user> <group>"
            bot.sendMessage(chat_id=update.message.chat_id, text=message)
            return

        message = "Being dev"

        bot.sendMessage(chat_id=update.message.chat_id, text=message)

from telegram.ext import CommandHandler
from telegram.parsemode import ParseMode
from utils.constants import HR, HR_HELP_DICT
from utils.decorator import requires_user_group
from business.hr import *

class HrCommand(object):
    """
        Provides user command handlers for HR department
    """

    def __init__(self, dispatcher):
        self.__dispatcher = dispatcher
        self.__register_handlers()

    def __register_handlers(self):
        """
            Registers the admin commands.
        """
        self.__dispatcher.add_handler(CommandHandler("hrhelp", self.__user_cmd_helps))
        self.__dispatcher.add_handler(CommandHandler("info", self.__info))
        self.__dispatcher.add_handler(CommandHandler("viewpto", self.__viewpto))

    
    @staticmethod
    @requires_user_group(HR)
    def __user_cmd_helps(update, context):
        """Command to show help
        """
        bot = context.bot
        help_dictionary = HR_HELP_DICT
        message = "*JARVIS* support HR those commands:\n\n"
        for key in help_dictionary.keys():
            message += help_dictionary[key]
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(HR)
    def __info(update, context):
        """Command to get information 
        """
        bot = context.bot
        args = context.args
        message = ""
        if len(args) > 1:
            message = "Syntax: info <employee_id>"
        else:
            employee_id = args[0]
            message = get_employee_info(employee_id)

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(HR)
    def __viewpto(update, context):
        """Command to view employee PTO request
        """
        bot = context.bot
        args = context.args
        message = ""
        if len(args) > 1:
            message = "Syntax: viewpto <employee_id>"
        else:
            employee_id = args[0]
            message = view_employee_pto(employee_id)

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )
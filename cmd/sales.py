from telegram.ext import CommandHandler
from telegram.parsemode import ParseMode
from utils.constants import SALES, SALES_HELP_DICT
from utils.decorator import requires_user_group
from business.sales import *

class SalesCommand(object):
    """
        Provides user command handlers for sales department
    """

    def __init__(self, dispatcher):
        self.__dispatcher = dispatcher
        self.__register_handlers()

    def __register_handlers(self):
        """
            Registers the admin commands.
        """
        self.__dispatcher.add_handler(CommandHandler("saleshelp", self.__sales_cmd_helps))
        self.__dispatcher.add_handler(CommandHandler("quota", self.__get_quota))
        self.__dispatcher.add_handler(CommandHandler("clientinfo", self.__get_clientinfo))

    @staticmethod
    @requires_user_group(SALES)
    def __sales_cmd_helps(update, context):
        """Command to show help
        """
        bot = context.bot
        help_dictionary = SALES_HELP_DICT
        message = "*JARVIS* support Sales those commands:\n\n"
        for key in help_dictionary.keys():
            message += help_dictionary[key]
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(SALES)
    def __get_quota(update, context):
        """Command to check monthly or quarterly sales quota
        """
        bot = context.bot
        args = context.args
        message = ""
        if len(args) > 0:
            message = "Syntax: quota"
        else:
            message = get_quota()

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )


    @staticmethod
    @requires_user_group(SALES)
    def __get_clientinfo(update, context):
        """Command to get client information
        """
        bot = context.bot
        args = context.args
        message = ""
        if len(args) > 1:
            message = "Syntax: clientinfo <client_id>"
        else:
            message = get_clientinfo(args[0])

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

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
        self.__dispatcher.add_handler(CommandHandler("saleshelp", self.__user_cmd_helps))
        self.__dispatcher.add_handler(CommandHandler("product_info", self.__product_info))
        self.__dispatcher.add_handler(CommandHandler("leaderboard", self.__leaderboard))

    @staticmethod
    @requires_user_group(SALES)
    def __user_cmd_helps(update, context):
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
    def __product_info(update, context):
        """Command to get product information
        """
        bot = context.bot
        args = context.args
        message = ""
        if len(args) > 1:
            message = "Syntax: product_info <product_id>"
        else:
            employee_id = args[0]
            message = get_product_by_id(employee_id)

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )


    @staticmethod
    @requires_user_group(SALES)
    def __leaderboard(update, context):
        """Command to get product information
        """
        bot = context.bot
        message = get_leaderboard()

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

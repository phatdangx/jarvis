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
        self.__dispatcher.add_handler(CommandHandler("hrhelp", self.__hr_cmd_helps))
        self.__dispatcher.add_handler(CommandHandler("holidaylist", self.__get_holidaylist))
        self.__dispatcher.add_handler(CommandHandler("training", self.__get_training_list))

    
    @staticmethod
    @requires_user_group(HR)
    def __hr_cmd_helps(update, context):
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
    def __get_holidaylist(update, context):
        """Command to get list of company holiday
        """
        bot = context.bot
        args = context.args
        message = ""
        if len(args) > 0:
            message = "Syntax: holidaylist"
        else:
            message = get_holidaylist()

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(HR)
    def __get_training_list(update, context):
        """Command to get list of company training
        """
        bot = context.bot
        args = context.args
        message = ""
        if len(args) > 0:
            message = "Syntax: training"
        else:
            message = get_training_list()

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )
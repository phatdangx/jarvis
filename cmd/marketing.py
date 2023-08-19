from telegram.ext import CommandHandler
from telegram.parsemode import ParseMode
from utils.constants import MARKETING, MAR_HELP_DICT
from utils.decorator import requires_user_group
from business.marketing import *

class MarketingCommand(object):
    """
        Provides user command handlers for marketing department
    """

    def __init__(self, dispatcher):
        self.__dispatcher = dispatcher
        self.__register_handlers()

    def __register_handlers(self):
        """
            Registers the admin commands.
        """
        self.__dispatcher.add_handler(CommandHandler("marhelp", self.__user_cmd_helps))
        self.__dispatcher.add_handler(CommandHandler("cp_track", self.__cp_track))
        self.__dispatcher.add_handler(CommandHandler("cp_list", self.__cp_list))

    @staticmethod
    @requires_user_group(MARKETING)
    def __user_cmd_helps(update, context):
        """Co.mmand to show help
        """
        bot = context.bot
        help_dictionary = MAR_HELP_DICT
        message = "*JARVIS* support Marketing those commands:\n\n"
        for key in help_dictionary.keys():
            message += help_dictionary[key]
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_to_message_id=update.message.message_id
        )
    
    @staticmethod
    @requires_user_group(MARKETING)
    def __cp_list(update, context):
        """Command to get list of marketing campaign
        """
        bot = context.bot
        args = context.args
        message = ""
        if len(args) > 1:
            message = "Syntax: cp_list <days>"
        else:
            days = args[0]
            message = list_all_campaign(days)

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )
    

    @staticmethod
    @requires_user_group(MARKETING)
    def __cp_track(update, context):
        """Command to get detail metric of a campaign
        """
        bot = context.bot
        args = context.args
        message = ""
        if len(args) > 1:
            message = "Syntax: cp_list <days>"
        else:
            cid = args[0]
            message = get_campaign_detail(cid)

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )
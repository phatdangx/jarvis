# -*- coding: utf-8 -*-
"""
    Provides the Jarvis UserCommands class.
"""
from telegram.parsemode import ParseMode
from telegram.ext import CommandHandler

from botheart.auth import requires_user_group
from botheart.utils import *

import time


class BDCommands(object):
    """
        Provides user command handlers
    """

    def __init__(self, dispatcher):
        self.__dispatcher = dispatcher
        self.__register_handlers()

    def __register_handlers(self):
        """
            Registers the BD commands.
        """
        self.__dispatcher.add_handler(CommandHandler("bdhelp", self.__bd_cmd_helps))
        self.__dispatcher.add_handler(CommandHandler("bfb", self.__block_fb, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("ufb", self.__unblock_fb, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("bp", self.__block_fb_page, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("up", self.__unblock_fb_page, pass_args=True))

    @staticmethod
    @requires_user_group(TECH, BD)
    def __bd_cmd_helps(update, context):
        """Command to show help
        """
        bot = context.bot
        help_dictionary = BD_HELP_DICT
        message = "*JARVIS* hỗ trợ BD các command sau:\n\n"
        for key in help_dictionary.keys():
            message += help_dictionary[key]
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH, BD)
    def __block_fb(update, context):
        """Command to block a personal facebook by facebook_id
        """
        bot = context.bot
        args = context.args
        if len(args) != 1:
            message = "Bạn truyền thiếu tham số. Cú pháp: bfb <fb_id>"
        else:
            message = block_fb(args[0])
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH, BD)
    def __unblock_fb(update, context):
        """Command to unblock a personal facebook by facebook_id
        """
        bot = context.bot
        args = context.args
        if len(args) != 1:
            message = "Bạn truyền thiếu tham số. Cú pháp: ufb <fb_id>"
        else:
            message = unblock_fb(args[0])
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH, BD)
    def __block_fb_page(update, context):
        """Command to block a facebook page by facebook_page_id
        """
        bot = context.bot
        args = context.args
        if len(args) != 1:
            message = "Bạn truyền thiếu tham số. Cú pháp: bp <page_id>"
        else:
            message = block_fb_page(args[0])
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH, BD)
    def __unblock_fb_page(update, context):
        """Command to unblock a facebook page by facebook_page_id
        """
        bot = context.bot
        args = context.args
        if len(args) != 1:
            message = "Bạn truyền thiếu tham số. Cú pháp: up <page_id>"
        else:
            message = unblock_fb_page(args[0])
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

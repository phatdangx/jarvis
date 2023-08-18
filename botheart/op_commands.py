# -*- coding: utf-8 -*-
"""
    Provides the Jarvis UserCommands class.
"""
from telegram.parsemode import ParseMode
from telegram.ext import CommandHandler

from botheart.auth import requires_user_group
from botheart.utils import *

import time


class OpCommands(object):
    """
        Provides user command handlers
    """

    def __init__(self, dispatcher):
        self.__dispatcher = dispatcher
        self.__register_handlers()

    def __register_handlers(self):
        """
            Registers the admin commands.
        """
        self.__dispatcher.add_handler(CommandHandler("ophelp", self.__op_cmd_helps))
        self.__dispatcher.add_handler(CommandHandler("ga", self.__get_lazada_address, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("uo", self.__update_lazada_origin_address, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("ud", self.__update_lazada_destination_address, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("rbt", self.__repush_lazada_order_by_tracking, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("aco", self.__auto_complete_order, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("ess", self.__enable_supplier_service, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("geo", self.__update_lazada_origin_geocoding, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("uwo", self.__update_waiting_order_record, pass_args=True))

    @staticmethod
    @requires_user_group(TECH, OP)
    def __op_cmd_helps(update, context):
        """Command to show help
        """
        bot = context.bot
        user = json.loads(redis_client.get(redis_key_pattern.format(update.message.from_user.id)))
        help_dictionary = OP_HELP_DICT
        message = "*JARVIS* hỗ trợ OP các command sau:\n\n"
        for key in help_dictionary.keys():
            message += help_dictionary[key]
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH, OP)
    def __get_lazada_address(update, context):
        """Command to get lazada origin and destination address by tracking_number
        """
        bot = context.bot
        args = context.args
        if len(args) != 1:
            message = "Bạn truyền thiếu tham số. Cú pháp: ga <tracking_number>"
        else:
            message = get_lzd_address_by_tracking_number(args[0])
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH, OP)
    def __update_lazada_origin_address(update, context):
        """Command to update LAZADA origin address
        """
        bot = context.bot
        args = context.args
        if len(args) < 2:
            message = "Bạn truyền thiếu tham số. Cú pháp: uo <tracking_number> <[new_address]>"
        else:
            tracking_number = args[0]
            message = update.message.text
            new_origin = message[message.find("[")+1:message.find("]")]
            message = update_lazada_origin_address(tracking_number, new_origin)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH, OP)
    def __update_lazada_destination_address(update, context):
        """Command to update LAZADA destination address
        """
        bot = context.bot
        args = context.args
        if len(args) < 2:
            message = "Bạn truyền thiếu tham số. Cú pháp: ud <tracking_number> <[new_address]>"
        else:
            tracking_number = args[0]
            message = update.message.text
            new_destination = message[message.find("[")+1:message.find("]")]
            message = update_lazada_destination_address(tracking_number, new_destination)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH, OP)
    def __repush_lazada_order_by_tracking(update, context):
        """Command to update LAZADA destination address
        """
        bot = context.bot
        args = context.args
        if len(args) < 1:
            message = "Bạn truyền thiếu tham số. Cú pháp: rpl <tracking_number>"
        else:
            tracking_number = args[0]
            message = repush_lazada_order_by_tracking_number(tracking_number)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH, OP)
    def __auto_complete_order(update, context):
        """Command to complete order automatically
        """
        bot = context.bot
        args = context.args
        if len(args) < 2:
            message = "Bạn truyền thiếu tham số. Cú pháp: aco <supplier_id> <list_order_id>"
        else:
            supplier_id = args[0]
            if supplier_id in KA_SUPPLIER_IDS:
                message_updates = update.message.text
                order_ids = message_updates[message_updates.find("[") + 1:message_updates.find("]")]
                message = auto_complete_orders(supplier_id, order_ids)
            else:
                message = "Supplier ID không nằm trong danh sách cho phép"
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )
       
    @staticmethod
    @requires_user_group(TECH, OP)
    def __enable_supplier_service(update, context):
        """Command to enable supplier service
        """
        bot = context.bot
        args = context.args
        if len(args) < 1:
            message = "Bạn truyền thiếu tham số. Cú pháp: ess <supplier_id>"
        else:
            supplier_id = args[0]
            message = enable_supplier_service(supplier_id)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH, OP)
    def __update_lazada_origin_geocoding(update, context):
        """Command to update LAZADA origin geocoding
        """
        bot = context.bot
        args = context.args
        if len(args) < 1:
            message = "Bạn truyền thiếu tham số. Cú pháp: geo <tracking_number>"
        else:
            tracking_number = args[0]
            message = update_lazada_origin_geocoding(tracking_number)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH, OP)
    def __update_waiting_order_record(update, context):
        """Command to update LAZADA origin geocoding
        """
        bot = context.bot
        args = context.args
        if len(args) < 2:
            message = "Bạn truyền thiếu tham số. Cú pháp: uwo <waiting_order_id>  <new_status>"
        else:
            wid = args[0]
            new_status = args[1]
            message = update_waiting_order_record(wid, new_status)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

# -*- coding: utf-8 -*-
"""
    Provides the Jarvis UserCommands class.
"""
from selectors import SelectorKey
from telegram.parsemode import ParseMode
from telegram.ext import CommandHandler

from botheart.auth import requires_user_group
from botheart.utils import *

import time


class UserCommands(object):
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
        self.__dispatcher.add_handler(CommandHandler("help", self.__user_cmd_helps))
        self.__dispatcher.add_handler(CommandHandler("cr", self.__check_refund, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("ccb", self.__check_callback, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("cb", self.__callback_partner, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("bo", self.__broadcast, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("rcs", self.__recom_stat, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("rp", self.__repush_partner_order, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("bso", self.__broadcast_stuck_orders, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("wld", self.__whitelist_device, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("co", self.__cancel_order, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("cd", self.__close_deal, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("complete", self.__complete_order, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("reset", self.__reset_child_order, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("city", self.__get_city_by_lat_lng, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("district", self.__get_district_by_lat_lng, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("trip", self.__plan_trip, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("countordertoday", self.__count_orders_today))
        self.__dispatcher.add_handler(CommandHandler("spa", self.__setup_partner_accounts, pass_args=True))
        self.__dispatcher.add_handler(CommandHandler("rfs", self.__refund_supplier, pass_args=True))

    @staticmethod
    @requires_user_group(TECH)
    def __user_cmd_helps(update, context):
        """Command to show help
        """
        bot = context.bot
        user = json.loads(redis_client.get(redis_key_pattern.format(update.message.from_user.id)))
        help_dictionary = TECH_HELP_DICT
        message = "*JARVIS* hỗ trợ các command sau:\n\n"
        for key in help_dictionary.keys():
            message += help_dictionary[key]
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH)
    def __check_refund(update, context):
        """Command to check if user is refunded by Momo
        """
        bot = context.bot
        args = context.args
        message = ""
        if len(args) < 2:
            message = "Bạn truyền thiếu tham số. Cú : check\_refund <payment-provider> <order-id>"
        else:
            payment_provider = args[0].upper()
            order_id = args[1]
            if payment_provider == "MOMO":
                message = check_momo_refund(order_id)

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH, OP)
    def __check_callback(update, context):
        """Command to check callback status for an order
        """
        bot = context.bot
        args = context.args
        if len(args) < 2:
            message = "Bạn truyền thiếu tham số. " \
                      + "Cú pháp: check\_callback <option> <order-id or tracking-number>\nOption: " \
                      + "[1]: check by order-id | [2]: check by tracking-number"
        else:
            option = int(args[0])
            _id = args[1]
            if option == 1:
                message = get_callback_history_by_order_id(_id)
            else:
                message = get_callback_history_by_tracking_number(_id)
        print(message)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH, OP)
    def __callback_partner(update, context):
        """Command to callback to sync status for partner
        """
        bot = context.bot
        args = context.args #https://docs.python-telegram-bot.org/en/v12.8/telegram.ext.callbackcontext.html?highlight=context%20args#telegram.ext.CallbackContext.args
        if len(args) < 2:
            message = "Bạn truyền thiếu tham số. Cú pháp: callback <OrderID> <\[Status\]> \n \
                       or Cú pháp: callback <OrderID1,OrderID2,OrderID3> <\[Status\]>  "
            bot.sendMessage(
                chat_id=update.message.chat_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN,
                reply_to_message_id=update.message.message_id
            )
        else:
            order_id = args[0]
            message = update.message.text
            order_status = message[message.find("[")+1:message.find("]")]
            order_ids = []
            if order_id.find(",") != -1:
                order_ids = args[0].split(",")
            else: 
                order_ids.append(order_id)
            for order_id in order_ids:
                message = call_partner_webhook(order_id, order_status)
                bot.sendMessage(
                    chat_id=update.message.chat_id,
                    text=message,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_to_message_id=update.message.message_id
                )
        
 

    @staticmethod
    @requires_user_group(TECH)
    def __broadcast(update, context):
        """Command to broadcast idle order
        """
        bot = context.bot
        args = context.args
        if len(args) < 1:
            message = "Bạn truyền thiếu tham số. Cú pháp: broadcast <OrderID>"
        else:
            order_id = args[0]
            message = broadcast_idle(order_id)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH)
    def __recom_stat(update, context):
        """Command to get recommend stats
        """
        bot = context.bot
        args = context.args
        if len(args) < 2:
            message = "Bạn truyền thiếu tham số. Cú pháp: rs <push-type> <last x hours >. Ex: rs socket 2"
        else:
            push_type = args[0]
            hour_ago = int(args[1])
            if hour_ago <= 24:
                to_time = int(time.time())
                from_time = to_time - hour_ago*3600
                message = rec_stat(push_type, from_time, to_time)
            else:
                message = "Chỉ có thể xem trong vòng 24h"
        logging.debug(message)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH)
    def __repush_partner_order(update, context):
        """Command to repush partner order
        """
        bot = context.bot
        args = context.args
        if len(args) < 2:
            message = "Bạn truyền thiếu tham số. Cú pháp: rp <partner> <last x hours >. Ex: rp lazada 2"
        else:
            partner = args[0]
            hour_ago = int(args[1])
            if hour_ago <= 48:
                to_time = int(time.time())
                from_time = to_time - hour_ago*3600
                message = repush_partner_order(partner, from_time, to_time)
            else:
                message = "Chỉ có thể re-push trong vòng 48h"
        logging.debug(message)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH)
    def __broadcast_stuck_orders(update, context):
        """Command to repush partner order
        """
        bot = context.bot
        args = context.args
        if len(args) < 1:
            message = "Bạn truyền thiếu tham số. Cú pháp: bso <last x hours >. Ex: bso 2"
        else:
            hour_ago = int(args[0])
            if hour_ago <= 48:
                to_time = int(time.time())
                from_time = to_time - hour_ago*3600
                message = broadcast_stuck_orders(from_time, to_time)
            else:
                message = "Chỉ có thể broadcast đơn trong vòng 48h"
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH)
    def __whitelist_device(update, context):
        """Command to whitelist device id
        """
        bot = context.bot
        args = context.args
        if len(args) < 3:
            message = "Bạn truyền thiếu tham số. Cú pháp: wld <device imei> <device owner> <department>. Ex: wld DE48DEDA-9F63-42D9-BB40-F20E6778E1BA Thang tech"
        else:
            device_imei = args[0]
            owner = args[1]
            department = args[2]
            user_name = update.message.from_user.name
            if not device_imei or device_imei == "":
                message = "Device IMEI không đúng format hoặc bị rỗng"
            elif not owner or owner == "":
                message = "Device owner không được để rỗng"
            elif not department or department == "":
                message = "Department không được để rỗng"
            else:
                message = whitelist_device(device_imei, owner, department, user_name)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH)
    def __cancel_order(update, context):
        """Command to whitelist device id
        """
        bot = context.bot
        args = context.args
        if len(args) < 3:
            message = "Bạn truyền thiếu tham số. Cú pháp: co <order id> <admin id> <comment>. Ex: co 21GM8OY3 84944309348 [Cancel by system]"
        else:
            order_id = args[0]
            admin_id = args[1]
            cancel_text = update.message.text
            comment = cancel_text[cancel_text.find("[")+1:cancel_text.find("]")]
            if not order_id or order_id == "":
                message = "Order ID empty"
            elif not admin_id or admin_id == "":
                message = "Admin ID empty"
            elif not comment or comment == "":
                message = "Comment empty"
            else:
                message = cancel_order(admin_id, order_id, comment)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH)
    def __close_deal(update, context):
        bot = context.bot
        args = context.args
        if len(args) < 1:
            message = "Bạn truyền thiếu tham số. Cú pháp: cd <deal id>. Ex: cd 6290362255955541b2d12701"
        else:
            deal_id = args[0]
            message = close_deal(deal_id)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH)
    def __complete_order(update, context):
        bot = context.bot
        args = context.args
        if len(args) < 1:
            m = "Bạn truyền thiếu tham số. Cú pháp: complete <order id>. Ex: complete 22XVVNDK"
        else:
            order_id = args[0]
            m = complete_order(order_id)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=m,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH)
    def __reset_child_order(update, context):
        bot = context.bot
        args = context.args
        if len(args) < 1:
            m = "Bạn truyền thiếu tham số. Cú pháp: reset <order id>. Ex: reset 22XVVNDK"
        else:
            order_id = args[0]
            m = reset_sameday_order_to_accepted(order_id)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=m,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH)
    def __get_city_by_lat_lng(update, context):
        bot = context.bot
        args = context.args
        if len(args) < 2:
            m = "Bạn truyền thiếu tham số. Cú pháp: city <lat> <lng>. Ex: city 10.8315392 106.6773514"
        else:
            lat = float(args[0])
            lng = float(args[1])
            m = get_city_by_lat_lng(lat, lng)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=m,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH)
    def __get_district_by_lat_lng(update, context):
        bot = context.bot
        args = context.args
        if len(args) < 2:
            m = "Bạn truyền thiếu tham số. Cú pháp: district <lat> <lng>. " \
                "Ex: district 10.8315392 106.6773514"
        else:
            lat = float(args[0])
            lng = float(args[1])
            m = get_district_by_lat_lng(lat, lng)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=m,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH)
    def __plan_trip(update, context):
        bot = context.bot
        args = context.args
        if len(args) < 2:
            m = "Bạn truyền thiếu tham số. Cú pháp: trip ENV ServiceID. " \
                "Ex: trip stg SGN-SAMEDAY"
        else:
            env = args[0]
            service_id = args[1]
            m = plan_trip_2h_4h(env, service_id)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=m,
            parse_mode=ParseMode.HTML,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH)
    def __count_orders_today(update, context):
        bot = context.bot
        m = stat_order_today()
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=m,
            parse_mode=ParseMode.HTML,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH)
    def __setup_partner_accounts(update, context):
        """Command create/update partner's user and supplier accounts
        """
        bot = context.bot
        args = context.args
        if len(args) < 3:
            message = "Bạn truyền thiếu tham số. Cú pháp: spa <mobile_numbers> <client_id> <client_email>"
        else:
            mobile_numbers = args[0]
            partner_id = args[1]
            partner_email = args[2]
            message = setup_partner_accounts(mobile_numbers, partner_id, partner_email)

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @requires_user_group(TECH)
    def __refund_supplier(update, context):
        """Command to refund money back to supplier when order cancellation is crashed
        """
        bot = context.bot
        args = context.args
        if len(args) < 2:
            message_resp = "Bạn truyền thiếu tham số. Cú pháp: rfs <supplier id> <order id>"
        else:
            supplier_id = args[0]
            order_id = args[1]
            message_resp = refund_supplier(supplier_id=supplier_id, order_id=order_id)

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=message_resp,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id
        )

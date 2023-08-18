#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Jarvis is a bot with ability to verify user before executing a command
"""

from telegram.ext import Updater, CommandHandler

from cmd.admin import AdminCommand
from cmd.hr import HrCommand
from cmd.marketing import MarketingCommand
from cmd.sales import SalesCommand
from utils.constants import TOKEN
from utils.decorator import *
from config import Config

import logging


@verify_user_init()
def start_handler(update, context):
    """Handle the command '/start'.

        Sends a greeting message to the client.
    """
    context.bot.sendMessage(
        chat_id=update.message.chat_id,
        text="Hi ! I am Jarvis. Run 'help' command to see what I can do",
        reply_to_message_id=update.message.message_id
    )


def main():
    """
        Main program of Jarvis
    """
    # Set up logging
    logger = logging.getLogger()
    log_level = Config["log_level"]
    logger.setLevel(log_level)

    # Updater
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_handler, pass_args=True))

    # Register commands
    AdminCommand(dispatcher)
    HrCommand(dispatcher)
    MarketingCommand(dispatcher)
    SalesCommand(dispatcher)


    # Polling update
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

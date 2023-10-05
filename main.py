#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Jarvis is a bot with ability to verify user before executing a command
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from cmd.admin import AdminCommand
from cmd.hr import HrCommand
from cmd.marketing import MarketingCommand
from cmd.sales import SalesCommand
from utils.constants import TOKEN, HR, MARKETING, SALES
from utils.decorator import *


@verify_user_init()
def start_handler(update, context):
    """Handle the command '/start'.

        Sends a greeting message to the client.
    """
    user = User(
        username=update.message.from_user.name,
        telegramid=update.message.from_user.id,
    )
    group = user.get_user_group()
    if group == HR:
        help_cmd = "hrhelp"
    elif group == MARKETING:
        help_cmd = "marhelp"
    elif group == SALES :
        help_cmd = "saleshelp"
    else:
        help_cmd = "help"

    context.bot.sendMessage(
        chat_id=update.message.chat_id,
        text="Hi ! I am Jarvis. Run '/{}' command to see what I can do".format(help_cmd),
        reply_to_message_id=update.message.message_id
    )


def unsupported_command(update, context):
    # Checking if the message starts with a '/'
    if update.message.text.startswith('/'):
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Sorry, I do not recognize that command.',
            reply_to_message_id=update.message.message_id
        )


def main():
    """
        Main program of Jarvis
    """

    # Updater
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_handler, pass_args=True))
    
    # Register commands
    AdminCommand(dispatcher)
    HrCommand(dispatcher)
    MarketingCommand(dispatcher)
    SalesCommand(dispatcher)

    # Handle unsupported commands
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unsupported_command))


    # Polling update
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

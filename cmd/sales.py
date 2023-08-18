from telegram.ext import CommandHandler

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
        self.__dispatcher.add_handler(CommandHandler("help", self.__user_cmd_helps))
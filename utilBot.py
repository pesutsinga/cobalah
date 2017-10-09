from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Updater
from time import gmtime, strftime


class ChopeBot:
    def __init__(self, token):
        self.firstOnline = strftime("%d %b %Y %H:%M:%S", gmtime()) + "GMT"
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.userPhase = {}

    def deploy(self):
        self.updater.start_polling()

    def add(self, handler):
        self.dispatcher.add_handler(handler)

    def handle_cmd(self, cmd, func):
        cmdHandler = CommandHandler(cmd, func)
        self.add(cmdHandler)

    def handle_msg(self, filter, func):
        msgHandler = MessageHandler(filter, func)
        self.add(msgHandler)

    def handle_callback(self, func):
        callbackHandler = CallbackQueryHandler(func)
        self.add(callbackHandler)

    def ask(self, bot, update, question, func):
        print("ini di ask kok")
        bot.send_message(
            chat_id=update.message.chat_id,
            text=question)
        self.set_phase(update, func)

    def phase(self, update):
        return self.userPhase.get(update.message.chat_id)

    def set_phase(self, update, func):
        self.userPhase[update.message.chat_id] = func

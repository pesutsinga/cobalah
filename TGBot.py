import logging
import telegram

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Updater
from time import gmtime, strftime


class TGBot:
    def __init__(self, token):
        self.firstOnline = strftime("%d %b %Y %H:%M:%S", gmtime())
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.userPhase = []

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
        bot.send_message(
            chat_id=update.message.chat_id,
            text=question)
        self.userPhase[update.message.from_user.username] = func

    def phase(self, chatID):
        self.userPhase[chatID]

from pprint import pprint
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import CallbackQueryHandler
from time import gmtime, strftime
import datetime
import logging


class TGBot:
    def __init__(self, token):
        self.firstOnline = strftime("%d %b %Y %H:%M:%S", gmtime())
        self.updater = Updater(token=token)
        self.dispatcher = updater.dispatcher

    def deploy():
        self.updater.start_polling()

    def add(handler):
        self.dispatcher.add_handler(handler)

    def handle_cmd(cmd, func):
        cmdHandler = CommandHandler(cmd, func)
        self.add(cmdHandler)

    def handle_msg(filter, func):
        msgHandler = MessageHandler(filter, func)
        self.add(msgHandler)

    def handle_callback(func):
        callbackHandler = CallbackQueryHandler(func)
        self.add(callbackHandler)


def function():
    pass

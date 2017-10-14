from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Updater
from time import localtime, strftime


class ChopeBot:
    def __init__(self, token):
        self.firstOnline = strftime("%d %b %Y %H:%M:%S", localtime())
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.userPhase = {}
        self.prioMessageID = {}
        self.captchaSolution = {}

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
        self.set_phase(update.message.chat_id, func)

    def phase(self, update):
        return self.userPhase.get(update.message.chat_id)

    def set_phase(self, chatID, func):
        self.userPhase[chatID] = func

    def set_prio_message_id(self, chatID, messageID):
        self.prioMessageID[chatID] = messageID

    def set_captcha_solution(self, chatID, solution):
        self.captchaSolution[chatID] = solution

    def get_captcha_solution(self, chatID):
        return self.captchaSolution.get(chatID)

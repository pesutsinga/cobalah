from TGBot import TGBot
from telegram.ext import Filters
from chopeDB import ChopeDB
from chopeBrowser import chopeBrowser
mainBot = None


def parrot(bot, update):
    print(update)
    bot.send_message(
        chat_id=update.message.chat_id,
        text=update.message.text)


def unknown_cmd(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Nigga. Damn. I don't understand your command fam")
    help_cmd(bot, update)
    # NOTE: jangan ganti user phase


def help_cmd(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="some random ass command list")
    pass


def username_check(bot, update):
    username = update.message.from_user.username
    if username is None:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="lu gada username, bikin dlu napa.. retry /start ya...")
        return False
    return True


def login_check(bot, update):
    chopeDB


def start_cmd(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="napa lw jing start gua")

    if not username_check(bot, update):
        return

    if not login_check(bot, update):
        return




def convo_handler(bot, update):
    func = mainBot.get_phase(update)
    if (func is not None):
        func(bot, update)
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="tulis /start dong... kita may have baru abis reboot")
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Baru on jam" + mainBot.firstOnline)


def main():
    mainBot = TGBot('377140861:AAEiMIj-VOwB68HcftvMILjr5wc6LJJml6g')
    mainBot.handle_msg(Filters.text, convo_handler)
    mainBot.handle_callback(convo_handler)
    mainBot.handle_cmd('start', start_cmd)
    mainBot.handle_cmd('help', help_cmd)
    mainBot.handle_msg(Filters.command, unknown_cmd)
    mainBot.deploy()


if __name__ == '__main__':
    main()

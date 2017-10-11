"""
    YA GW TAU INI BELOM JADI
    maafkan segala dosaku kawan" ...
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters
from utilBot import ChopeBot
import utilBrowser
import utilDB
mainBot = None


def parrot(bot, update):
    print(update)
    bot.send_message(
        chat_id=update.message.chat_id,
        text=update.message.text)


def unknown_cmd(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="I can't understand your command")
    help_cmd(bot, update)


def help_cmd(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="some random ass command list")
    pass


def tgusername_check(bot, update):
    username = update.message.from_user.username
    if username is not None:
        return True
    return False


def ask_username(bot, update):
    global mainBot
    mainBot.ask(bot, update, "username apaan ?", ans_username)


def ans_username(bot, update):
    global mainBot
    utilDB.set_username(
        tgUsername=update.message.from_user.username,
        username=update.message.text)
    ask_password(bot, update)


def ask_password(bot, update):
    global mainBot
    mainBot.ask(bot, update, "password apaan ?", ans_password)


def ans_password(bot, update):
    global mainBot
    print('huehuehue')
    utilDB.set_password(
        tgUsername=update.message.from_user.username,
        password=update.message.text,
        chatID=update.message.chat_id)
    print('slds')
    start_cmd(bot, update)


def login_check(bot, update):
    username = update.message.from_user.username
    chatID = update.message.chat_id
    usr = utilDB.get_username(username)
    print('lalala')
    pwd = utilDB.get_password(username, chatID)
    print('lololo')
    print(chatID)
    print(usr)
    print(pwd)
    canLogin = utilBrowser.try_login(usr, pwd)
    print(canLogin)
    return canLogin


def start_cmd(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Let me first run some checks")

    if not tgusername_check(bot, update):
        bot.send_message(
            chat_id=update.message.chat_id,
            text="bikin username dlu sana /start")
        return

    print("user have username")

    if not login_check(bot, update):
        ask_username(bot, update)
        return

    print("user can log in")

    bot.send_message(
        chat_id=update.message.chat_id,
        text="SUCCESSFUL")

    prio_cmd(bot, update)


def prio_text(tgUsername):
    listPrio = utilDB.get_prio(tgUsername)
    listPrio = [(k, v) for k, v in listPrio.items()]
    listPrio.sort()
    print(listPrio)
    msg = ""
    for key, val in listPrio:
        msg += str(key).replace('_', ' ').title() + ": " + str(val) + "\n"
    return msg


def prio_markup():
    keyboard = [
        [
            InlineKeyboardButton(
                "Change prio",
                callback_data='callback_prio_set|change prio'),

            InlineKeyboardButton(
                "Accept prio",
                callback_data='callback_prio_set|accept prio')
        ],
        [
            InlineKeyboardButton(
                "What does the number mean",
                callback_data='callback_prio_set|help prio')
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def prio_cmd(bot, update):
    global mainBot
    bot.send_message(
        chat_id=update.message.chat_id,
        text="here is the list of your prio")

    msg = prio_text(update.message.from_user.username)

    prio_msg = bot.send_message(
        chat_id=update.message.chat_id,
        text=msg,
        reply_markup=prio_markup())

    mainBot.set_prio_message_id(update.message.chat_id, prio_msg.message_id)
    print(prio_msg.message_id)


def order_cmd(bot, update):
    pass


def convo_handler(bot, update):
    global mainBot
    func = mainBot.phase(update)
    if (func is not None):
        func(bot, update)
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="tulis /start dong... kita may have baru abis reboot")

        bot.send_message(
            chat_id=update.message.chat_id,
            text="Baru on jam" + mainBot.firstOnline)


def callback_handler(bot, update):
    global mainBot
    callbackData = update.callback_query.data
    print(callbackData)
    dats = callbackData.split('|', 1)
    if (dats[0] == 'callback_prio_set'):
        callback_prio_set(bot, update, dats[1])
    elif (dats[0] == 'settings'):
        username = update.callback_query.from_user.username
        x = dats[1].split('||', 1)
        colName = x[0].upper().replace(' ', '_')
        utilDB.set_prio(username, colName, x[1])
        chatID = update.callback_query.message.chat_id
        bot.edit_message_text(
            chat_id=chatID,
            message_id=mainBot.prioMessageID[chatID],
            text=prio_text(username),
            reply_markup=prio_markup())


def callback_prio_set(bot, update, task):
    chatID = update.callback_query.message.chat_id
    if (task == 'change prio'):
        change_prio(bot, update)
    elif (task == 'accept prio'):
        bot.send_message(
            chat_id=chatID,
            text='hai')
    elif (task == 'help prio'):
        bot.send_message(
            chat_id=chatID,
            text='dasar kaw anak ikan gini aja gangerti :v')


def change_prio(bot, update):
    chatID = update.callback_query.message.chat_id

    seats = [
        "Circular Pods",
        "Collab Booths",
        "Learning Pods",
        "Learning Room",
        "Recording Room"]

    for seat in seats:
        keyboard = []
        for i in range(6):
            button = InlineKeyboardButton(
                    "__" + str(i) + "__",
                    callback_data="settings|" + seat + "||" + str(i))
            keyboard.append(button)
        reply_markup = InlineKeyboardMarkup([keyboard])
        bot.send_message(
            chat_id=chatID,
            text=seat + " :",
            reply_markup=reply_markup)


def main():
    global mainBot
    mainBot = ChopeBot('377140861:AAEiMIj-VOwB68HcftvMILjr5wc6LJJml6g')
    mainBot.handle_msg(Filters.text, convo_handler)
    mainBot.handle_cmd('start', start_cmd)
    mainBot.handle_cmd('changeusername', ask_username)
    mainBot.handle_cmd('prio', prio_cmd)
    mainBot.handle_cmd('help', help_cmd)
    mainBot.handle_callback(callback_handler)
    mainBot.handle_msg(Filters.command, unknown_cmd)
    mainBot.deploy()


if __name__ == '__main__':
    main()

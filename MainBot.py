"""
    YA GW TAU INI BELOM JADI
    maafkan segala dosaku kawan" ...
"""
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters
from utilBot import ChopeBot
import utilBrowser
import utilDB
import pprint
import string
import random
from io import BytesIO
from captcha.image import ImageCaptcha
mainBot = None


def parrot(bot, update):
    print(update)
    bot.send_message(
        chat_id=update.message.chat_id,
        text=update.message.text)


@run_async
def unknown_cmd(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="I can't understand your command")
    help_cmd(bot, update)


@run_async
def help_cmd(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="some random ass command list")
    pass


@run_async
def tgusername_check(bot, update):
    username = update.message.from_user.username
    if username is not None:
        return True
    return False


@run_async
def ask_username(bot, update):
    global mainBot
    mainBot.ask(bot, update, "username apaan ?", ans_username)


@run_async
def ans_username(bot, update):
    global mainBot
    utilDB.set_username(
        tgUsername=update.message.from_user.username,
        username=update.message.text)
    ask_password(bot, update)


@run_async
def ask_password(bot, update):
    global mainBot
    mainBot.ask(bot, update, "password apaan ?", ans_password)


@run_async
def ans_password(bot, update):
    global mainBot
    print('huehuehue')
    utilDB.set_password(
        tgUsername=update.message.from_user.username,
        password=update.message.text,
        chatID=update.message.chat_id)
    print('slds')
    start_cmd(bot, update)


@run_async
def login_check(bot, update):
    username = update.message.from_user.username
    chatID = update.message.chat_id
    usr = utilDB.get_username(username)
    pwd = utilDB.get_password(username, chatID)
    print(chatID)
    print(usr)
    print(pwd)
    canLogin = utilBrowser.try_login(usr, pwd)
    print(canLogin)
    return canLogin


@run_async
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


@run_async
def prio_text(tgUsername):
    listPrio = utilDB.get_prio(tgUsername)
    listPrio = [(k, v) for k, v in listPrio.items()]
    listPrio.sort()
    print(listPrio)
    msg = ""
    for key, val in listPrio:
        msg += str(key).replace('_', ' ').title() + ": " + str(val) + "\n"
    return msg


@run_async
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


@run_async
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


@run_async
def order_cmd(bot, update):
    pass


@run_async
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


@run_async
def callback_handler(bot, update):
    global mainBot
    callbackData = update.callback_query.data
    print(callbackData)
    data = callbackData.split('|', 1)
    if (data[0] == 'callback_prio_set'):
        callback_prio_set(bot, update, data[1])
    elif (data[0] == 'settings'):
        username = update.callback_query.from_user.username
        changes = data[1].split('||', 1)
        colName = changes[0].upper().replace(' ', '_')
        value = changes[1]
        utilDB.set_prio(username, colName, value)

        chatID = update.callback_query.message.chat_id
        bot.edit_message_text(
            chat_id=chatID,
            message_id=mainBot.prioMessageID[chatID],
            text=prio_text(username),
            reply_markup=prio_markup())

        seatName = update.callback_query.message.text.strip(": ")
        keyboard = []
        for i in range(6):
            pad = "**" if str(i) == str(value) else "__"
            button = InlineKeyboardButton(
                    pad + str(i) + pad,
                    callback_data="settings|" + seatName + "||" + str(i))
            keyboard.append(button)
        reply_markup = InlineKeyboardMarkup([keyboard])

        bot.edit_message_text(
            chat_id=chatID,
            message_id=update.callback_query.message.message_id,
            text=update.callback_query.message.text,
            reply_markup=reply_markup)
        print('asdfadsf')


def find_seat(tgUsername, chatID):
    usr = utilDB.get_username(tgUsername)
    pwd = utilDB.get_password(tgUsername, chatID)
    print(usr, pwd)
    instances = utilBrowser.ChopeBrowser()
    occupied = instances.scrape_seats(usr, pwd)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(occupied)
    return occupied


@run_async
def ask_captcha(bot, update, callback=False):
    global mainBot
    if callback:
        chatID = update.callback_query.message.chat_id
    else:
        chatID = update.message.chat_id

    if (not callback):
        if mainBot.get_captcha_solution(chatID) == update.message.text:
            bot.send_message(
                chat_id=chatID,
                text="please wait, be calm, this may take 3 min")
            find_seat(update.message.from_user.username, chatID)
            return

    image = ImageCaptcha(
        fonts=['fonts/Inconsolata-g.ttf', 'fonts/RobotoSlab-Regular.ttf'])
    randStr = ''.join(random.choice(
        string.ascii_lowercase + string.digits) for _ in range(6))
    data = image.generate(randStr)
    print('hehshe')
    assert isinstance(data, BytesIO)
    image.write(randStr, 'curCaptcha.png')
    print('afeois')

    mainBot.set_phase(chatID, ask_captcha)
    print('sfle')
    bot.send_photo(chat_id=chatID, photo=open('curCaptcha.png', 'rb'))
    bot.send_message(chat_id=chatID, text="please write the captcha")
    print("alsdkfa")
    mainBot.set_captcha_solution(chatID, randStr)


@run_async
def callback_prio_set(bot, update, task):
    chatID = update.callback_query.message.chat_id
    if (task == 'change prio'):
        change_prio(bot, update)
    elif (task == 'accept prio'):
        bot.send_message(
            chat_id=chatID,
            text='hai')
        ask_captcha(bot, update, True)
    elif (task == 'help prio'):
        bot.send_message(
            chat_id=chatID,
            text='dasar kaw anak ikan gini aja gangerti :v')


@run_async
def change_prio(bot, update):
    chatID = update.callback_query.message.chat_id

    seats = [
        "Circular Pods",
        "Collab Booths",
        "Learning Pods",
        "Learning Room",
        "Recording Room"]

    prioList = utilDB.get_prio(update.callback_query.from_user.username)
    for seat in seats:
        val = prioList[seat.upper().replace(' ', '_')]
        print(val)
        keyboard = []
        for i in range(6):
            pad = "**" if i == val else "__"
            button = InlineKeyboardButton(
                    pad + str(i) + pad,
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

"""
    YA GW TAU INI BELOM JADI
    maafkan segala dosaku kawan" ...
"""
from captcha.image import ImageCaptcha
from datetime import datetime
from functools import wraps
from io import BytesIO
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters
from telegram.ext.dispatcher import run_async
from utilBot import ChopeBot
import os
import pprint
import random
import sys
import time
import utilBrowser
import utilDB


LIST_OF_ADMINS = [412231900]
START_TIME = {}
END_TIME = {}
mainBot = None


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def parrot(bot, update):
    print(update)
    bot.send_message(
        chat_id=update.message.chat_id,
        text=update.message.text)


def tgusername_check(bot, update):
    username = update.message.from_user.username
    if username is not None:
        return True
    return False

@run_async
def ask_username(bot, update):
    global mainBot
    mainBot.ask(bot, update, "Your NTU Username ?", ans_username)

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
    mainBot.ask(bot, update, "Your NTU Password ?", ans_password)

@run_async
def ans_password(bot, update):
    global mainBot
    print('huehuehue')
    utilDB.set_password(
        tgUsername=update.message.from_user.username,
        password=update.message.text,
        chatID=update.message.chat_id)
    start_cmd(bot, update)

@run_async
def ask_start_chope(bot, update, callback=False):
    print("lsdkfsdf'")
    if callback:
        chatID = update.callback_query.message.chat_id
    else:
        chatID = update.message.chat_id

    global mainBot
    bot.send_message(
        chat_id=chatID,
        text="start time  HH:MM ?")
    mainBot.set_phase(chatID, ans_start_chope)


@run_async
def ans_start_chope(bot, update):
    strTime = update.message.text
    strTime = strTime.strip(' ')
    strTime = strTime.split(':')
    try:
        print(strTime)
        hour = int(strTime[0])
        minute = int(strTime[1])
        if not (9 <= hour < 21):
            print(1/0)
        if not (0 <= minute < 60):
            print(1/0)
        START_TIME[update.message.chat_id] = update.message.text.strip(' ')
        ask_end_chope(bot, update)
    except:
        ask_start_chope(bot, update)

@run_async
def ask_end_chope(bot, update):
    global mainBot
    mainBot.ask(bot, update, "until  HH:MM ?", ans_end_chope)

@run_async
def ans_end_chope(bot, update):
    strTime = update.message.text
    strTime = strTime.strip(' ')
    strTime = strTime.split(':')
    try:
        hour = int(strTime[0])
        minute = int(strTime[1])
        if not (9 <= hour < 21):
            print(1/0)
        if not (0 <= minute < 60):
            print(1/0)
        END_TIME[update.message.chat_id] = update.message.text.strip(' ')
        ask_captcha(bot, update, 1, None)
    except:
        ask_end_chope(bot, update)

@run_async
def ask_captcha(bot, update, numnum, pctype, callback=False):
    global mainBot
    if numnum == 1:
        chatID = update.message.chat_id
        msgLower = update.message.text.lower()
        solnLower = str(mainBot.get_captcha_solution(chatID)).lower()
        print()
        print("asdfa")
        if msgLower == solnLower:
            print("asalll")
            bot.send_message(
                chat_id=chatID,
                text="please wait, be calm, this may take 2 min")
            print(str(datetime.now()))
            occupied = check_seat(update.message.from_user.username, chatID)
            print_seat(bot, update, occupied)
            return
    if numnum == 2:
        print('asdasaaa')
        chatID = update.callback_query.message.chat_id
        bot.send_message(
                chat_id=chatID,
                text="please wait")
        print("okaaay")
        print(update.callback_query.from_user.username)
        check_pc(bot, update, update.callback_query.from_user.username, chatID, pctype)
        return
    image = ImageCaptcha(
        fonts=['fonts/captcha.ttf'])
    unambiguousChars = '23456789abcdefghkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
    randStr = ''.join(random.choice(unambiguousChars) for _ in range(6))
    mainBot.set_captcha_solution(chatID, randStr)
    data = image.generate(randStr)
    assert isinstance(data, BytesIO)
    image.write(randStr, 'curCaptcha.png')

    mainBot.set_phase(chatID, ask_captcha)
    bot.send_photo(chat_id=chatID, photo=open('curCaptcha.png', 'rb'))
    bot.send_message(chat_id=chatID, text="please write the captcha")


def check_pc(bot, update, tgUsername, chatID, pctype):
    print(tgUsername)
    usr = utilDB.get_username(tgUsername)
    pwd = utilDB.get_password(tgUsername, chatID)
    print(usr)
    instances = utilBrowser.ChopeBrowser()
    result = instances.pc_setup(usr, pwd, pctype)
    if result[1] == 'booked':
        bot.send_message(chat_id=chatID, text="Successfully booked, this is your seat: " + result[0])
    else:
        bot.send_message(chat_id=chatID, text="Cannot book")


def login_check(bot, update):
    username = update.message.from_user.username
    chatID = update.message.chat_id
    usr = utilDB.get_username(username)
    pwd = utilDB.get_password(username, chatID)
    canLogin = utilBrowser.try_login(usr, pwd)
    return canLogin


def check_seat(tgUsername, chatID):
    usr = utilDB.get_username(tgUsername)
    pwd = utilDB.get_password(tgUsername, chatID)
    instances = utilBrowser.ChopeBrowser()
    occupied = instances.scrape_seats(usr, pwd)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(occupied)
    print(str(datetime.now()))
    return occupied

@run_async
def start_cmd(bot, update):
    global mainBot
    chatID = update.message.chat_id
    mainBot.prioMessageID[chatID] = None
    mainBot.captchaSolution[chatID] = None
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


def unknown_cmd(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="I can't understand your command")
    help_cmd(bot, update)


def help_cmd(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="just /start and /changeusername")
    pass


def prio_text(tgUsername):
    listPrio = utilDB.get_prio(tgUsername)
    listPrio = [(k, v) for k, v in listPrio.items()]
    listPrio.sort()
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
        ],
        [
            InlineKeyboardButton(
                "PC booking",
                callback_data='callback_prio_set|PC')
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
            text="first online: " + mainBot.firstOnline)


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
    elif (data[0] == 'takepc'):
        ask_captcha(bot, update, 2, data[1], True)


def enc_time(time):
    print('time')
    print(time)
    time = time.split(':')
    print(time)
    hour = int(time[0])
    print(hour)
    minute = int(time[1])
    print(minute)
    print(hour, minute)
    return 2 * hour + minute // 30


def print_seat(bot, update, occ, tom=0):
    chatID = update.message.chat_id
    occLen = len(occ)
    nSeat = occLen // 2

    tgUsername = update.message.from_user.username
    castePrio = utilDB.get_prio(tgUsername)
    casteName = [
        "Circular Pods",
        "Collab Booths",
        "Learning Pods",
        "Recording Room",
        "Video Conferencing Room"]

    seatName = [occ[i] for i in range(0, occLen, 2)]

    seatType = []
    seatType.extend([0] * 2)
    seatType.extend([1] * 12)
    seatType.extend([0] * 1)
    seatType.extend([2] * 6)
    seatType.extend([4] * 1)
    seatType.extend([3] * 1)
    seatType.extend([0] * 2)

    seatPrio = [castePrio[casteName[seat].upper().replace(' ', '_')] for seat in seatType]

    for i in range(nSeat):
        print(seatName[i], casteName[seatType[i]], seatPrio[i])

    seatOcc = [occ[i] for i in range(1, occLen, 2)]

    today = datetime.now().weekday()
    # nnt hapus
    today -= 1

    for i in range(nSeat):
        seatOcc[i] = seatOcc[i][today]

    occTable = []
    for i in range(nSeat):
        occTable.append([seatPrio[i]] * 50)

    seatName.append("seatless")
    occTable.append([0] * 50)

    print(occTable)

    print('hololo')
    for i in range(nSeat):
        print(seatName[i])
        print(seatOcc[i])

    for i in range(nSeat):
        seat = seatOcc[i]
        print(seat)
        for dura in seat:
            print(dura)
            st = enc_time(dura[0])
            en = enc_time(dura[1])
            print(st, en)
            for k in range(st, en):
                occTable[i][k] = 0

    stTime = enc_time(START_TIME[chatID])
    enTime = enc_time(END_TIME[chatID])

    print('horehorehore123123123')
    lastTake = nSeat
    cumLen = -1
    for j in range(stTime, enTime):
        curBest = nSeat
        cumLen += 1
        for i in range(nSeat):
            print('slelskdf')
            if occTable[i][j] >= occTable[curBest][j]:
                curBest = i

        print(curBest)
        if lastTake != curBest:
            if cumLen == 0:
                continue
            print('lol')
            print(seatName[lastTake])
            print(cumLen)
            soln = "take " + seatName[lastTake] + " for" + str(cumLen) + " blocks"
            print(soln)

            bot.send_message(
                chat_id=chatID,
                text=soln)
            lastTake = curBest
            cumLen = 0

    soln = "take " + seatName[lastTake] + " for" + str(cumLen + 1) + " blocks"
    bot.send_message(
        chat_id=chatID,
        text=soln)

    print('horhorhor')

    for j in range(stTime, enTime):
        for i in range(nSeat):
            print(occTable[i][j], end=' ')
        print()

@run_async
def callback_prio_set(bot, update, task):
    chatID = update.callback_query.message.chat_id
    if (task == 'change prio'):
        change_prio(bot, update)
    elif (task == 'accept prio'):
        ask_start_chope(bot, update, True)
    elif (task == 'help prio'):
        bot.send_message(
            chat_id=chatID,
            text='dasar kaw anak ikan gini aja gangerti :v')
    elif (task == 'PC'):
        PC_markup(bot, update)


def PC_markup(bot, update):
    chatID = update.callback_query.message.chat_id
    keyboard = [
        [
            InlineKeyboardButton(
                "Single Monitors",
                callback_data='takepc| (1) Single Monitors')
        ],
        [
            InlineKeyboardButton(
                "Dual Monitors",
                callback_data='takepc|(2) Dual Monitors')
        ],
        [
            InlineKeyboardButton(
                "Triple Monitors",
                callback_data='takepc|(3) Triple Monitors'),
        ],
        [
            InlineKeyboardButton(
                "Curved Monitors",
                callback_data='takepc|Curved Monitors')
        ]
    ]
    xxx = InlineKeyboardMarkup(keyboard)
    bot.send_message(
            chat_id=chatID,
            text="Choose your PC",
            reply_markup=xxx)

@run_async
def change_prio(bot, update):
    chatID = update.callback_query.message.chat_id

    seats = [
        "Circular Pods",
        "Collab Booths",
        "Learning Pods",
        "Recording Room",
        "Video Conferencing Room"]

    prioList = utilDB.get_prio(update.callback_query.from_user.username)
    for seat in seats:
        val = prioList[seat.upper().replace(' ', '_')]
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


@restricted
def reboot(bot, update):
    bot.send_message(update.message.chat_id, "Bot is restarting...")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)


def main():
    print('Bot is prepared')
    global mainBot
    TOKEN = "406125095:AAEiPIwPMdD18XA39VtAplp5L7MdUm0cFEM"
    # TOKEN = "377140861:AAEiMIj-VOwB68HcftvMILjr5wc6LJJml6g"
    mainBot = ChopeBot(TOKEN)
    mainBot.handle_msg(Filters.text, convo_handler)
    mainBot.handle_cmd('start', start_cmd)
    mainBot.handle_cmd('changeusername', ask_username)
    mainBot.handle_cmd('prio', prio_cmd)
    mainBot.handle_cmd('help', help_cmd)
    mainBot.handle_cmd('r', reboot)
    mainBot.handle_callback(callback_handler)
    mainBot.handle_msg(Filters.command, unknown_cmd)
    mainBot.deploy()
    print('Deployed')


if __name__ == '__main__':
    main()

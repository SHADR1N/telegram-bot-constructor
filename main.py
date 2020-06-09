import telebot
from telebot import types
from telebot import apihelper
import sqlite3
from models import *
import os
import config
from config import *
from collections import defaultdict
import logging
bot = telebot.TeleBot(token)


listDIR = os.listdir(path=MENU)
userDIR = defaultdict(list)

db.create_tables([Users])


def messload(message):
    txt = message.text
    for me in Users.select():
        user_id = me.user_id
        bot.send_message(user_id, txt)

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data=i) for i in [i for i in listDIR]])
    keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data=i) for i in ['Рассылка по пользователям']])
    bot.send_message(message.chat.id, 'Сообщение отправленно!', reply_markup=keyboard, parse_mode="Html")


@bot.message_handler(commands=["start"])
def start(message):
    global listDIR

    user_id = message.chat.id
    print(user_id)
    if not Users.user_exists(user_id):
        bot.send_message(ADMIN, 'Новый пользователь!', parse_mode="Html")
        Users.create_user(user_id)

    logging.basicConfig(filename="app.log",format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info("User {} start bot".format(message.chat.id))

    if message.chat.id == ADMIN:
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data=i) for i in [i for i in listDIR]])
        keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data=i) for i in ['Рассылка по пользователям']])
        bot.send_message(message.chat.id, 'Стартовое сообщение', reply_markup=keyboard, parse_mode="Html")

    else:

        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data=i) for i in [i for i in listDIR]])
        bot.send_message(message.chat.id, 'Стартовое сообщение', reply_markup=keyboard, parse_mode="Html")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print(call.data)
    global listDIR
    ID = call.message.chat.id

    if call.data == 'Рассылка по пользователям':
        samp = bot.send_message(ADMIN, 'Введите текст сообщения:')
        bot.register_next_step_handler(samp, messload)

    elif call.data == 'Назад':
        if not userDIR[call.message.chat.id]:
            logging.basicConfig(filename="app.log",format='%(asctime)s - %(message)s', level=logging.INFO)
            logging.info("User {} join to Main menu".format(call.message.chat.id))
            if not userDIR[call.message.chat.id]:
                keyboard = types.InlineKeyboardMarkup(row_width=3)
                keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data=i) for i in [i for i in listDIR]])
                bot.send_message(call.message.chat.id, 'Главное меню', reply_markup=keyboard, parse_mode="Html")


            else:
                del userDIR[call.message.chat.id]

                keyboard = types.InlineKeyboardMarkup(row_width=3)
                keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data=i) for i in [i for i in listDIR]])
                bot.send_message(call.message.chat.id, 'Главное меню', reply_markup=keyboard, parse_mode="Html")

        else:


            del userDIR[call.message.chat.id][-1]  # Удаляет из словаря последний каталог в который перешли кнопка НАЗАД

            Saved_dir_to_user = '\\'.join(str(v) for v in userDIR[call.message.chat.id]) # Переводит список в строку
            main = '{}\\{}'.format(MENU, Saved_dir_to_user) # Скаладывает абсолютный путь и то что мы на открывали

            logging.basicConfig(filename="app.log",format='%(asctime)s - %(message)s', level=logging.INFO)
            logging.info("User {} join to {}".format(call.message.chat.id, main))

            directory = os.chdir(main) # Должен открыть папку по пути main но не открывает выбивает в самое начало 
            print(  os.getcwd()  ) # Выводит собственно путь


            for file in os.listdir(path = directory):

                if file.endswith(".txt"):
                    txt = os.path.join(main, file)
                    open_txt = open(txt, 'r')
                    mess = open_txt.read()

                    bot.send_message(ID, mess)

                if file.endswith(".jpg"):
                    img = os.path.join(main, file)
                    open_img = open(img, 'rb')

                    bot.send_photo(ID, open_img)

            Saved_dir_to_user = '\\'.join(str(v) for v in userDIR[call.message.chat.id])
            main = MENU + '\\' + Saved_dir_to_user
            New_listDIR = os.listdir(path=main)
            listdir = []
            for file in New_listDIR:
                if file.endswith('.txt'):
                    pass
                elif file.endswith('.jpg'):
                    pass
                elif file.endswith('.jpeg'):
                    pass
                elif file.endswith('.db'):
                    pass
                else:
                    listdir.append(file)

            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data=i) for i in [i for i in listdir]])
            keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data=i) for i in ['Назад', 'Главное меню']])
            bot.send_message(call.message.chat.id, 'Каталог меню', reply_markup=keyboard, parse_mode="Html")
    
    elif call.data == 'Главное меню':
        logging.basicConfig(filename="app.log",format='%(asctime)s - %(message)s', level=logging.INFO)
        logging.info("User {} join to Main menu".format(call.message.chat.id))
        if not userDIR[call.message.chat.id]:
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data=i) for i in [i for i in listDIR]])
            bot.send_message(call.message.chat.id, 'Главное меню', reply_markup=keyboard, parse_mode="Html")


        else:
            del userDIR[call.message.chat.id]

            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data=i) for i in [i for i in listDIR]])
            bot.send_message(call.message.chat.id, 'Главное меню', reply_markup=keyboard, parse_mode="Html")

    elif call.data != 'Назад' or call.data != 'Главное меню':
        Saved_dir_to_user = '\\'.join(str(v) for v in userDIR[call.message.chat.id])
        main = MENU + '\\' + Saved_dir_to_user
        print(main+'But')

        logging.basicConfig(filename="app.log",format='%(asctime)s - %(message)s', level=logging.INFO)
        logging.info("User {} join to {}".format(call.message.chat.id, main))

        directory = os.chdir(main)
        Check_data = os.listdir(directory)

        userDIR[call.message.chat.id].append(call.data)

        Saved_dir_to_user = '\\'.join(str(v) for v in userDIR[call.message.chat.id])
        main = MENU + '\\' + Saved_dir_to_user
        try:
            directory = os.chdir(main)
        except FileNotFoundError:
            call.data = 'Главное меню'

        New_listDIR = os.listdir(directory)

        if call.data in listDIR or call.data in Check_data:

            for file in os.listdir(directory):

                if file.endswith(".txt"):
                    txt = os.path.join(main, file)
                    open_txt = open(txt, 'r')
                    mess = open_txt.read()

                    bot.send_message(ID, mess)

                if file.endswith(".jpg"):
                    img = os.path.join(main, file)
                    open_img = open(img, 'rb')

                    bot.send_photo(ID, open_img)

                if file.endswith(".png"):
                    img = os.path.join(main, file)
                    open_img = open(img, 'rb')

                    bot.send_photo(ID, open_img)

                if file.endswith(".jpeg"):
                    img = os.path.join(main, file)
                    open_img = open(img, 'rb')

                    bot.send_photo(ID, open_img)

                if file.endswith(".gif"):
                    img = os.path.join(main, file)
                    open_img = open(img, 'rb')

                    bot.send_photo(ID, open_img)

            Saved_dir_to_user = '\\'.join(str(v) for v in userDIR[call.message.chat.id])
            main = MENU + '\\' + Saved_dir_to_user
            New_listDIR = os.listdir(path=main)
            listdir = []
            for file in New_listDIR:
                if file.endswith('.txt'):
                    pass
                elif file.endswith('.jpg'):
                    pass
                elif file.endswith('.jpeg'):
                    pass
                else:
                    listdir.append(file)

            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data=i) for i in [i for i in listdir]])
            keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data=i) for i in ['Назад', 'Главное меню']])
            bot.send_message(ID, 'Каталог меню', reply_markup=keyboard, parse_mode="Html")







if __name__ == '__main__':
    bot.polling(none_stop=True)
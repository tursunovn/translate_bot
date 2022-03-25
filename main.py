from configs import *
from telebot import TeleBot
from googletrans import Translator

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help', 'history'])
def command_start(message):
    chat_id = message.chat.id
    if message.text == '/start':
        bot.send_message(chat_id, f"""Привет {message.from_user.first_name}
Я бот перевода или определения слов и текста""")
    elif message.text == '/help':
        bot.send_message(chat_id, f""" Данный бот был создан да просто скопирован, если есть 
вопросы то это ваши проблемы учить надо было """)




bot.polling(none_stop=True)
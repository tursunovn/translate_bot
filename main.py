from configs import *
from telebot import TeleBot
from googletrans import Translator

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help', 'history'])
def command_start(message):
    print(message)



bot.polling(none_stop=True)
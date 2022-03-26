from configs import *
from telebot import TeleBot
from googletrans import Translator
from keyboards import *

bot = TeleBot(TOKEN, parse_mode='HTML')

@bot.message_handler(commands=['start', 'help', 'history'])
def command_start(message):
    chat_id = message.chat.id
    if message.text == '/start':
        msg = bot.send_message(chat_id, f"""Привет<b> {message.from_user.first_name}</b>
Я бот перевода или определения слов и текста""", reply_markup=generate_phone_number())
        cursor.execute('''SELECT * FROM users WHERE telegram_id=?''', (chat_id,))
        user = cursor.fetchone()
        if user:
            bot.send_message(chat_id, 'Что желаете сделать?', reply_markup=choose_command())
        else:
            bot.register_next_step_handler(msg, register_user)

    elif message.text == '/help':
        bot.send_message(chat_id, f""" Данный бот был создан да просто <b>скопирован,</b> если есть 
вопросы то это ваши проблемы учить надо было """)
    elif message.text == 'history':
        bot.send_message(chat_id, 'Ваша история')



def register_user(message):
    chat_id = message.chat.id
    try:
        first_name = message.from_user.first_name
        username = message.from_user.username
        phone = message.contact.phone_number

        cursor.execute('''
            INSERT INTO users(telegram_id, first_name, username, phone) VALUES
            (?,?,?,?);
        ''', (chat_id, first_name, username, phone))

        db.commit()
        msg = bot.send_message(chat_id, 'Что желаете сделать?', reply_markup=choose_command())
    except:
        msg = bot.send_message(chat_id, 'НАЖМИТЕ на кнопку!! ', reply_markup=generate_phone_number())
        bot.register_next_step_handler(msg, register_user)


@bot.message_handler(regexp=r'Перевод \U0001F913')
def translate_start(message):
    chat_id = message.chat.id
    word = bot.send_message(chat_id, 'Введите слово или текст которые хотите перевесте')
    bot.register_next_step_handler(word, translation)
    

@bot.message_handler(regexp=r'Определение \U0001F9D0')
def definition_start(message):
    chat_id = message.chat.id
    word = bot.send_message(chat_id, 'Введите слово или текст которые хотите определить')

def translation(message):
    chat_id = message.chat.id
    translator = Translator(service_urls=['translate.google.com'])
    word = message.text
    english_word = translator.translate(text=word, dest='en').text

    cursor.execute('''
    SELECT user_id FROM users WHERE telegram_id = ?;
    ''', (chat_id,))
    user_id = cursor.fetchone()[0]

    cursor.execute('''
    INSERT INTO history_translation(user_id, user_text, translate_text) VALUES
    (?,?,?)
    ''', (chat_id, word, english_word))
    bot.send_message(chat_id, english_word)
    msg = bot.send_message(chat_id, 'Что желаете сделать?', reply_markup=choose_command())

bot.polling(none_stop=True)
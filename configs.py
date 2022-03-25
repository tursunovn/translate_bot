import sqlite3

db = sqlite3.connect('bot.db', check_same_thread=False)

cursor = db.cursor()

TOKEN = '5230881826:AAExr6R1esgN-eHMmuPT1htr2j_GqN-W9zc'
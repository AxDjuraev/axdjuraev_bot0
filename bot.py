
from telebot import TeleBot
from time import sleep
API = '5306057698:AAFtg7O014soJoSreLDUXYZEOEN_liKTGwk';
bot = TeleBot(API)
@bot.message_handler()
def doSomething(person):
  id = person.chat.id 
  message = person.text
  bot.send_message(id,f'You said: {message}')

id = ''

while True:
  bot.send_message(id, 'bot working...')
  sleep(4)
# bot.polling()

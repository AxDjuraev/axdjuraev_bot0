
from telebot import TeleBot
from time import sleep
from pytube import YouTube

API = '5306057698:AAFtg7O014soJoSreLDUXYZEOEN_liKTGwk'
bot = TeleBot(API)
@bot.message_handler()
def downloadYoutubeVideo(video_link):
  youtube_video = YouTube(link)
  streams = youtube_video.streams.filter(res='360p', progressive="True")
  file_name = streams.first().download()
  return file_name
def doSomething(person):
  id = person.chat.id 
  try:
    message = person.text
    strippedMessage = message.strip()
    if not strippedMessage.startswith('/'):
      bot.send_message(id, f'function not found. Try send message "/help"')
      return
    
  except Exception as exception:
    bot.send_message(id, f'error: "{str(exception)}" and try again.')
# id = '1722229628'

# while True:
#   bot.send_message(id, 'bot working...')
#   sleep(6)
if __name__ == "__main__":
  bot.polling()

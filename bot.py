
from telebot import TeleBot
from time import sleep
from pytube import YouTube
from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

API = '5306057698:AAFtg7O014soJoSreLDUXYZEOEN_liKTGwk'
bot = TeleBot(API)

admin_id = '1722229628'

def downloadYoutubeVideo(video_link):
  youtube_video = YouTube(video_link)
  streams = youtube_video.streams.filter(res='360p', progressive="True")
  file_name = streams.first().download()
  return file_name
def sendYoutubeVideo(id, message):
  file_full_name = downloadYoutubeVideo(message.split()[1])
  file_name = file_full_name[file_full_name.rfind('/')+1:]
  bot.send_video(id, open(file_full_name,'rb'), caption = file_name)
@bot.message_handler()
def doSomething(person):
  id = person.chat.id 
  try:
    message = person.text
    strippedMessage = message.strip()
    if not strippedMessage.startswith('/'):
      bot.send_message(id, f'Try send message "/help"')
      return
    function = (strippedMessage.split(' ')[0])[1:]
    if not function in functions.keys():
      bot.send_message(id, f'function not found. Try send message "/help"')
    functions[function].__call__(id, strippedMessage)
  except Exception as exception:
    bot.send_message(id, f'error: "{str(exception)}" fix and try again.')

functions = {
  'tube': lambda id, message: sendYoutubeVideo(id, message),
   'help': lambda id, message: bot.send_message(id, 'welcom to group')
}
if __name__ == "__main__":
  bot.polling()

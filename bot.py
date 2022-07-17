import os
from telebot import TeleBot
from time import sleep
from pytube import YouTube
from selenium import webdriver
from bs4 import BeautifulSoup

API = '5306057698:AAFtg7O014soJoSreLDUXYZEOEN_liKTGwk'
bot = TeleBot(API)

admin_id = '1722229628'

active_numbers_website_domain = 'https://www.number4sms.com'

last_entered_number = ''

def getPageSource(url):
  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  wd = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
  wd.get(url)
  page_source = wd.page_source
  wd.close()
  return page_source

def sendPage(id, message):
  url = message.split()[1]
  with open('1.html','w') as f:
    f.write(getPageSource(url))
  bot.send_document(id, open('1.html','r'))

def getCountries():
  countries = {}
  page_source = getPageSource(active_numbers_website_domain)
  soup = BeautifulSoup(page_source)
  for country in soup.find_all('div',{'class': 'col-md-3 col-12 text-center number-grid-element'}):
    link = country.find_all('a')[0]['href']
    name = country.find_all('p')[0].text
    countries[name.lower()] = link
  return countries

def getNumbersWithSources(page_source):
  numbers = {}
  soup = BeautifulSoup(page_source)
  div_content = soup.find_all('div',{'id': 'other-numbers'})[0]
  nums = div_content.find_all('a')
  for number in nums:
    numbers[number.text] = number["href"]
  return numbers

def findFromArray(item, array):
  for array_item in array:
    if item.lower() in array_item.lower():
      return array_item
  raise ValueError('Not Found in Numbers.')
def getLastMessages(number, limit=3):
  last_messages = []
  countries = getCountries()
  numbers = {}
  for country in countries:
    link = countries[country]
    url = f'{active_numbers_website_domain}/{countries[country]}'
    page_source = getPageSource(url)
    numbers.update(getNumbersWithSources(page_source))
  number_source = numbers[findFromArray(number, numbers)]
  url = f'{active_numbers_website_domain}{number_source}'
  page_source = getPageSource(url)
  soup = BeautifulSoup(page_source)
  count = 3
  messages = soup.find_all('div',{'class': 'message-bubble'})
  for message in messages:
    last_message = {}
    from_ = message.find_all('div',{'class': 'message-bubble-from'})[0].text 
    date  = message.find_all('div',{'class': 'message-bubble-time'})[0].text
    text  = message.find_all('div',{'class': 'message-bubble-text'})[0].text
    last_message['from'] = from_
    last_message['date'] = date
    last_message['text'] = text
    last_messages.append(last_message)
  return messages

def sendNums(id, message):
  countries = getCountries()
  if len(message.split()) < 2:
    bot.send_message(id, ' \n'.join(countries.keys()))
    return
  country = message.split()[1].lower()
  url = f'{active_numbers_website_domain}/{countries[country]}'
  page_source = getPageSource(url)
  numbers = getNumbersWithSources(page_source)
  bot.send_message(id, ' \n'.join(numbers.keys()))
    

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
      return
    functions[function].__call__(id, strippedMessage)
  except Exception as exception:
    bot.send_message(id, f'error: "{str(exception)}" fix and try again.')

def sendLastMessage(id, message):
  global last_entered_number
  answer = ''
  if len(message.split()) < 2:
    if last_entered_number.strip() == '': 
      bot.send_message(id, 'choose a number.')
      return
    number = '/message '+last_entered_number
  number = ''.join(message.split()[1:])
  last_messages = getLastMessages(number)
  answer += f'number: {number}'
  for message in last_messages:
    answer += f'from: {message["from"]}\ntext: {message["text"]}\ndate: {message["date"]}'
  bot.send_message(id, answer)
  last_entered_number = number 

functions = {
  'tube':     lambda id, message: sendYoutubeVideo(id, message),
   'help':    lambda id, message: bot.send_message(id, 'welcom to group'),
   'page':    lambda id, message: sendPage(id, message),
   'nums':    lambda id, message: sendNums(id, message),
   'messages':lambda id, message: sendLastMessage(id, message)
}
if __name__ == "__main__":
  bot.polling()

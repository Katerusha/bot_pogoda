# import json
# from re import search

import telebot  #PyTelegramBotApipip
import wikipedia
import requests
from selenium import webdriver
from time import sleep
# from pyowm import OWM
# from pyowm.utils.config import get_default_config


bot = telebot.TeleBot('8080004615:AAFQPxaLPt0PvVU9EVBXQt74iUZBLk91amY')
pogoda = 'f883de52a272b801e142e8d73e40d2d2'

# def pogodaa(city:str):
#     config = get_default_config()
#     config["language"] = 'ru'
#     owm = OWM(pogoda, config)
#     manager = owm.weather_manager()
#     novorossiysk = manager.weather_at_places(city)
#     get = novorossiysk.weather
#     status = get.detailed_status
#     temp = get.temperature('celsius')
#     tempe = round(temp['temp'])
#     oshushenia = round(temp['feels_like'])
#     message = f'in city{city} now {status} {tempe} it feels like {oshushenia}'
#     print(message)
#     return message

driver = webdriver.Edge() #браузер


@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, 'привет ты можешь спросить меня что угодно и я могу ответить на твои вопромы')

@bot.message_handler(commands = ['wikipedia'])
def wikipedia(message):
    mes = bot.send_message(message.chat.id, 'введите что хотите найти')
    bot.register_next_step_handler(mes, getwiki)  # ждать получения информации


@bot.message_handler(commands = ['ya'])
def ya(message):
    mes = bot.send_message(message.chat.id, 'введи текст который ты хочешь найти')
    bot.register_next_step_handler(mes, botsearch) #ждать получения информации

@bot.message_handler(commands = ['city'])
def city(message):
    mes = bot.send_message(message.chat.id, 'введи город погоду которого ты хочешь найти')
    bot.register_next_step_handler(mes, poisk) #ждать получения информации


@bot.message_handler(content_types = ['text'])
def get_text_messages(message):
    # mes = message.text
    # if mes == 'найди':
    #     search(mes)
    bot.send_message(message.chat.id, 'если хочешь начать поиск веди команду /start или /ya, или /city для поиска города и его информации')

def poisk(message):
    global pogoda, driver
    url = 'https://api.openweathermap.org/data/2.5/weather?q='+message.text+'&units=metric&lang=ru&appid='+ pogoda
    driver.get(url)
    print(url)
    weather = requests.get(url).json()
    # weather_data = json.dumps(weather,indent=2)
    temp = round(weather['main']['temp'])
    temp_sea = round(weather['main']['sea_level'])
    temp_feelslike = round(weather['main']['feels_like'])
    bot.send_message(message.chat.id,f'Сейчас в городе {temp} градусов\nОщущается как {temp_feelslike} градусов\nСейчас уровень воды в море {temp_sea} метра')


def getwiki(message):
    mas = message.text
    wikipedia.set_lang('ru')
    result = wikipedia.search(mas)
    page = wikipedia.page(result[0])
    title = page.title
    kategorii = page.categories
    text = page.content
    links = page.links
    summar = page.summary
    silka = page.url
    bot.send_message(message.chat.id, f'вот что я нашел{title}, {summar}\n тут есть все {silka}')


def botsearch(message):
    global driver, link
    bot.send_message(message.chat.id, 'начинаю поиск')
    # for i in message:
    #     if i == ' ':
    #         i = '+'
    link = (f'https://ya.ru/search/?text={message.text}')
    driver.get(link)
    sleep(2)



bot.polling(none_stop = True, interval = 0)
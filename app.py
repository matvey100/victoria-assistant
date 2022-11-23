'''
Прототип голосового помощника
Для работы требуются следующие зависимости: pip install pyaudio wikipedia-api google pyttsx3 chardet SpeechRecognition
Также требуется установить следующие библиотеки из репозитория https://github.com/RHVoice/RHVoice/blob/master/doc/ru/Binaries.md
SAPI 5 для Windows / NVDA для Linux и Macintosh
    * Языковой пакет Английский
    * Аглийский - Evgeniy-eng
    * Русский - Anna

All rights reserved.
2022
'''
# from vosk import Model, KaldiRecognizer  # оффлайн-распознавание от Vosk
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
# import wave  # создание и чтение аудиофайлов формата wav
# import json  # работа с json-файлами и json-строками
# import os  # работа с файловой системой
import pyttsx3  # Синтез речи
import webbrowser  # Работа с браузером
import chardet  # определение языка речи
# from googlesearch import search  # поиск в google
import traceback  # вывод traceback без остановки работы программы при отлове исключений
import wikipediaapi  # найти в википедии
import random  # модуль рандомайзера
# import googletrans  # модуль переводчика

'''Инициализация синтеза речи'''
tts = pyttsx3.init()
voices = tts.getProperty('voices')
# Задать голос по умолчанию
tts.setProperty('voice', 'ru')
# Попробовать установить предпочтительный голос
for voice in voices:
    ru = voice.id.find('RHVoice\Anna')  # Найти Анну от RHVoice
    if ru > -1: # если нашли, выбираем этот голос
        tts.setProperty('voice', voice.id)

tts.say('Привет, Создатель!')
tts.runAndWait()
# tts.say('Hi, user!')
# tts.runAndWait()

def play_voice_assistant_speech(text_to_speech):
    """
    Проигрывание речи ответов голосового ассистента (без сохранения аудио)
    :param text_to_speech: текст, который нужно преобразовать в речь
    """
    tts.say(str(text_to_speech))
    tts.runAndWait()

def record_and_recognize_audio(*args: tuple):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""
        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)
        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 10, 15)
        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return
        # использование online-распознавания через Google
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()
        except speech_recognition.UnknownValueError:
            pass
        # в случае проблем с доступом в Интернет происходит выброс ошибки
        except speech_recognition.RequestError:
            print("Check your Internet Connection, please")
        return recognized_data

def search_for_video_on_youtube(*args: tuple):
    """
    Поиск видео на YouTube с автоматическим открытием ссылки на список результатов
    :param args: фраза поискового запроса
    """
    if not args[0]: return
    search_term = " ".join(args[0])
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open(url)

    # для мультиязычных голосовых ассистентов лучше создать
    # отдельный класс, который будет брать перевод из JSON-файла
    if lang == 'Russian':
        print("Вот что я нашла по запросу " + search_term + "в ютуб.")
        play_voice_assistant_speech("Вот что я нашла по запросу " + search_term + "в ютуб.")
    else:
        print("Here is what I found for " + search_term + "on youtube")
        play_voice_assistant_speech("Here is what I found for " + search_term + "on youtube")

def play_greetings(*args: tuple):
    '''Приветствие пользователя'''
    if lang == 'Russian':
        print('Привет, пользователь! Я - голосовой помощник Виктория. Чем я могу пом+очь вам?')
        play_voice_assistant_speech('Привет, пользователь! Я - голосовой помощник Виктория. Чем я могу пом+очь вам?')
    else:
        print('Hello, user! I am - voice assistant Victoria. How can I help you?')
        play_voice_assistant_speech('Hello, user! I am - voice assistant Victoria. How can I help you?')

def play_farewell_and_quit(*args: tuple):
    """
    Проигрывание прощательной речи и выход
    """
    if lang == 'Russian':
        print("До свидания! Хорошего дня!")
        play_voice_assistant_speech("До свидания! Хорошего дня!")
    else:
        print('Goodbye! Have a good day!')
        play_voice_assistant_speech('Goodbye! Have a good day!')
    tts.stop()
    quit()

def search_for_term_on_google(*args: tuple):
    """
    Поиск в Google с автоматическим открытием ссылок (на список результатов и на сами результаты, если возможно)
    :param args: фраза поискового запроса
    """
    if not args[0]: return
    search_term = " ".join(args[0])
    # открытие ссылки в браузере
    url = "https://google.com/search?q=" + search_term
    webbrowser.get().open(url)
    # альтернативный поиск с автоматическим открытием ссылок на результаты (в некоторых случаях может быть небезопасно)
    # search_results = []
    # try:
    #     for _ in search(search_term,  # что искать
    #                     tld="com",  # верхнеуровневый домен
    #                     lang='ru',  # используется язык, на котором говорит ассистент
    #                     num=1,  # количество результатов на странице
    #                     start=0,  # индекс первого извлекаемого результата
    #                     stop=1,  # индекс последнего извлекаемого результата (я хочу, чтобы открывался первый результат)
    #                     pause=1.0,  # задержка между HTTP-запросами
    #                     ):
    #         search_results.append(_)
    #         webbrowser.get().open(_)
    #
    # # поскольку все ошибки предсказать сложно, то будет произведен отлов с последующим выводом без остановки программы
    # except:
    #     play_voice_assistant_speech("Seems like we have a trouble. See logs for more information")
    #     traceback.print_exc()
    #     return
    # print(search_results)
    if lang == 'Russian':
        print(('Вот что я нашла по запросу {}.').format(search_term))
        play_voice_assistant_speech(('Вот что я нашла по запросу {}.').format(search_term))
    else:
        print(("Here is what I found for {} on google").format(search_term))
        play_voice_assistant_speech(("Here is what I found for {} on google").format(search_term))

def search_for_definition_on_wikipedia(*args: tuple):
    """
    Поиск в Wikipedia определения с последующим озвучиванием результатов и открытием ссылок
    :param args: фраза поискового запроса
    """
    if not args[0]: return
    search_term = " ".join(args[0])
    # установка языка (в данном случае используется язык, на котором говорит ассистент)
    wiki = wikipediaapi.Wikipedia('ru')
    # поиск страницы по запросу, чтение summary, открытие ссылки на страницу для получения подробной информации
    wiki_page = wiki.page(search_term)
    try:
        if wiki_page.exists():
            if lang == 'Russian':
                print(("Вот что я нашла по запросу {} в Википедии").format(search_term))
                play_voice_assistant_speech(("Вот что я нашла по запросу {} в Википедии").format(search_term))
            else:
                print(("Here is what I found for {} on Wikipedia").format(search_term))
                play_voice_assistant_speech(("Here is what I found for {} on Wikipedia").format(search_term))
            webbrowser.get().open(wiki_page.fullurl)
            # чтение ассистентом первых двух предложений summary со страницы Wikipedia
            # (могут быть проблемы с мультиязычностью)
            play_voice_assistant_speech(wiki_page.summary.split(".")[:2])
        else:
            # открытие ссылки в браузере в случае, если на Wikipedia не удалось найти ничего по запросу
            if lang == 'Russian':
                print("Такой информации нет в Википедии, вот результаты в google.")
                play_voice_assistant_speech("Такой информации нет в Википедии, вот результаты в google.")
            else:
                print(("Can't find {} on Wikipedia. But here is what I found on google").format(search_term))
                play_voice_assistant_speech(("Can't find {} on Wikipedia. But here is what I found on google").format(search_term))
            url = "https://google.com/search?q=" + search_term
            webbrowser.get().open(url)
    # поскольку все ошибки предсказать сложно, то будет произведен отлов с последующим выводом без остановки программы
    except:
        print("Seems like we have a trouble. See logs for more information")
        play_voice_assistant_speech("Seems like we have a trouble. See logs for more information")
        traceback.print_exc()
        return

def flip_a_coin(*args: tuple):
    l = random.randint(0, 2)
    if l == 0:
        if lang == 'Russian':
            print('Орёл!')
            play_voice_assistant_speech('Орёл!')
        else:
            print('Heads!')
            play_voice_assistant_speech('Heads!')
    else:
        if lang == 'Russian':
            print('Решка!')
            play_voice_assistant_speech('Решка!')
        else:
            print('Tails!')
            play_voice_assistant_speech('Tails!')
    return

def name_trigger(*args: tuple):
    if lang == 'Russian':
        print('Чем я могу пом+очь?')
        play_voice_assistant_speech('Чем я могу пом+очь?')
    else:
        print('How can I help you?')
        play_voice_assistant_speech('How can I help you?')

def execute_command_with_name(command_name: str, *args: list):
    """
    Выполнение заданной пользователем команды с дополнительными аргументами
    :param command_name: название команды
    :param args: аргументы, которые будут переданы в функцию
    :return:
    """
    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
        else:
            # if lang == 'Russian':
            #     play_voice_assistant_speech('Такой команды не существует.')
            #     print('Такой команды не существует.')
            #     pass
            # else:
            #     play_voice_assistant_speech("Command not found")
            #     print("Command not found")
            #     pass
            pass

'''Команды для помощника'''
commands = {
    ('подбрось', 'heads'): flip_a_coin,
    ("hello", "hi", "morning", "привет"): play_greetings,
    ("bye", "goodbye", "quit", "exit", "stop", "пока", 'хватит'): play_farewell_and_quit,
    ('victoria', 'вика', 'виктория'): name_trigger,
    ("search", "google", "find", "найди"): search_for_term_on_google,
    ("video", "youtube", "watch", "видео", 'ютуб'): search_for_video_on_youtube,
    ("wikipedia", "definition", "about", "определение", "википедия"): search_for_definition_on_wikipedia,
    # ("translate", "interpretation", "translation", "перевод", "перевести", "переведи"): get_translation,
    # ("weather", "forecast", "погода", "прогноз"): get_weather_forecast
}

if __name__ == "__main__":
    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    while True:
        # старт записи речи с последующим выводом распознанной речи
        # и удалением записанного в микрофон аудио
        voice_input = record_and_recognize_audio()
        # os.remove("microphone-results.wav")
        print(voice_input)
        about_lang = dict.values(chardet.detect(voice_input[0].encode('cp1251')))  # определение распознаваемого языка
        lang = [*about_lang][2]
        # print(lang)

        # отделение комманд от дополнительной информации (аргументов)
        voice_input = voice_input.split(" ")
        command = voice_input[0]
        command_options = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
        execute_command_with_name(command, command_options)

"""
Prototype of a voice assistant

The following dependencies are required to work:
pip install pyaudio wikipedia-api google pyttsx3 chardet SpeechRecognition deep-translator

You also need to install the following libraries from RHVoice repositories (https://github.com/RHVoice/RHVoice/blob/master/doc/ru/Binaries.md):
SAPI 5 for Windows / NVDA for Linux and Macintosh
   * Language Pack English
   * English — Evgeniy-eng
   * Russian — Anna

All rights reserved
2023
"""
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import pyttsx3  # Синтез речи
import webbrowser  # Работа с браузером
import traceback  # вывод traceback без остановки работы программы при отлове исключений
import wikipediaapi  # найти в википедии
import random  # модуль рандомайзера
from deep_translator import GoogleTranslator  # модуль переводчика

"""Инициализация синтеза речи"""
tts = pyttsx3.init()
voices = tts.getProperty("voices")
# Задать голос по умолчанию
tts.setProperty("voice", "ru")
# Попробовать установить предпочтительный голос
for voice in voices:
    ru = voice.id.find("RHVoice\Anna")  # Найти Анну от RHVoice
    if ru > -1:  # если нашли, выбираем этот голос
        tts.setProperty("voice", voice.id)


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
            play_voice_assistant_speech("Пожалуйста, проверьте соединение с Интернетом!")
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
    print("Вот что я нашла по запросу " + search_term + " в ютуб.")
    play_voice_assistant_speech("Вот что я нашла по запросу " + search_term + " в ютуб.")


def play_greetings(*args: tuple):
    """
    Приветствие пользователя
    """
    print("Привет, пользователь! Я - голосовой помощник Виктория. Чем я могу помочь вам?")
    play_voice_assistant_speech("Привет, пользователь! Я - голосовой помощник Виктория. Чем я могу пом+очь вам?")


def play_farewell_and_quit(*args: tuple):
    """
    Проигрывание прощальной речи и выход
    """
    print("До свидания! Хорошего дня!")
    play_voice_assistant_speech("До свидания! Хорошего дня!")
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
    #                     lang="ru",  # используется язык, на котором говорит ассистент
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
    print("Вот что я нашла по запросу {}.".format(search_term))
    play_voice_assistant_speech("Вот что я нашла по запросу {}.".format(search_term))


def search_for_definition_on_wikipedia(*args: tuple):
    """
    Поиск в Wikipedia определения с последующим озвучиванием результатов и открытием ссылок
    :param args: фраза поискового запроса
    """
    if not args[0]: return
    search_term = " ".join(args[0])
    # установка языка (в данном случае используется язык, на котором говорит ассистент)
    wiki = wikipediaapi.Wikipedia("ru")
    # поиск страницы по запросу, чтение summary, открытие ссылки на страницу для получения подробной информации
    wiki_page = wiki.page(search_term)
    try:
        if wiki_page.exists():
            print("Вот что я нашла по запросу {} в Википедии".format(search_term))
            play_voice_assistant_speech("Вот что я нашла по запросу {} в Википедии".format(search_term))
            webbrowser.get().open(wiki_page.fullurl)
            # чтение ассистентом первых двух предложений summary со страницы Wikipedia
            # (могут быть проблемы с мультиязычностью)
            play_voice_assistant_speech(wiki_page.summary.split(".")[:2])
        else:
            # открытие ссылки в браузере в случае, если на Wikipedia не удалось найти ничего по запросу
            print("Такой информации нет в Википедии, вот результаты в google.")
            play_voice_assistant_speech("Такой информации нет в Википедии, вот результаты в google.")
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
        print("Орёл!")
        play_voice_assistant_speech("Орёл!")
    else:
        print("Решка!")
        play_voice_assistant_speech("Решка!")
    return


def name_trigger(*args: tuple):
    print("Чем я могу помочь?")
    play_voice_assistant_speech("Чем я могу пом+очь?")
    
    print(
    "Доступные команды: ",
    "Приветствие:                Привет",
    "Помощь (выводит это меню):  Помощь; Виктория",
    "Закончить разговор:         Пока; Хватит; Стоп",
    "Подбросить монетку:         Подбрось монетку; Heads or tails",
    "Запустить переводчик:       Перевод; Перевести; Переведи",
    "Искать в Google:            Найди; гугл; <запрос>",
    "Искать в Википедии:         Найди в википедии; википедия; <запрос>",
    "Искать в Ютуб:              ютуб; youtube <запрос>",
    "(Продолжение следует...)",
sep="\n"
)


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
            pass


def insert_context(command):
    """
    Извлечение кодового слова из строки
    :param command:
    :return:
    """
    s = command.split()
    if s[0] == "найди" and (s[1] == "видео" or s[1] == "определение" or s[1] == "перевод" or s[1] == "ютуб"):
        s = s[1::]
    elif s[0] == "найди" and s[1] == "в" and (s[2] == "википедии" or s[2] == "ютубе" or s[2] == "google" or s[2] == "гугл" or s[2] == "youtube"):
        s = s[2::]
    else: pass
    new = " ".join(s)
    return new


def get_translation(*args: tuple):
    """
    Переводчик
    :param args:
    :return:
    """
    print("Запускаю навык 'Перевод'!")
    play_voice_assistant_speech("Запускаю навык 'Перевод'!")
    play_voice_assistant_speech("Говорите целевой язык.")
    lang = record_and_recognize_audio()
    if lang == "русский":
        target = "ru"
    else:
        target = "en"
    play_voice_assistant_speech("Говорите фразу для перевода.")
    to_translate = record_and_recognize_audio()
    translated = GoogleTranslator(source='auto', target=target).translate(to_translate)
    print(translated)
    play_voice_assistant_speech(translated)
    return


"""
Команды для помощника
(пока только для русского языка)
"""
commands = {
    ("подбрось", "heads"): flip_a_coin,
    ("hello", "hi", "morning", "привет", "здорова", "хэй"): play_greetings,
    ("bye", "goodbye", "quit", "exit", "stop", "пока", "хватит", "стоп"): play_farewell_and_quit,
    ("victoria", "help", "вика", "виктория", "помощь"): name_trigger,
    ("search", "google", "find", "найди", "погода", "прогноз", "гугл", "интернет", "интернете"): search_for_term_on_google,
    ("video", "youtube", "watch", "видео", "ютуб"): search_for_video_on_youtube,
    ("wikipedia", "definition", "about", "определение", "википедия", "википедии"): search_for_definition_on_wikipedia,
    ("translate", "interpretation", "translation", "перевод", "перевести", "переведи"): get_translation,
}


print("Привет, пользователь! Я - голосовой помощник Виктория. Вот что я могу.")
play_voice_assistant_speech("Привет, пользователь! Я - голосовой помощник Виктория. Вот что я могу.")

print(
    "Доступные команды: ",
    "Приветствие:                Привет",
    "Помощь (выводит это меню):  Помощь; Виктория",
    "Закончить разговор:         Пока; Хватит; Стоп",
    "Подбросить монетку:         Подбрось монетку; Heads or tails",
    "Запустить переводчик:       Перевод; Перевести; Переведи",
    "Искать в Google:            Найди; гугл; <запрос>",
    "Искать в Википедии:         Найди в википедии; википедия; <запрос>",
    "Искать в Ютуб:              ютуб; youtube <запрос>",
    "(Продолжение следует...)",
sep="\n"
)


if __name__ == "__main__":
    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    while True:
        # старт записи речи с последующим выводом распознанной речи
        # и удалением записанного в микрофон аудио
        voice_input = record_and_recognize_audio()
        print('Пользователь:', voice_input)

        # отделение комманд от дополнительной информации (аргументов)
        if len(voice_input) != 0:
            voice_input = insert_context(voice_input)
            voice_input = voice_input.split(" ")
            command = voice_input[0]
            command_options = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
            execute_command_with_name(command, command_options)
        else: pass

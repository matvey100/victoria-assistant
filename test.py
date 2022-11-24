# import pyttsx3
#
# tts = pyttsx3.init() # Инициализировать голосовой движок.
# voices = tts.getProperty('voices')
# for voice in voices:
#     print('=======')
#     print('Имя: %s' % voice.name)
#     print('ID: %s' % voice.id)
#     print('Язык(и): %s' % voice.languages)
#     print('Пол: %s' % voice.gender)
#     print('Возраст: %s' % voice.age)

# import pyttsx3
# tts = pyttsx3.init()
# voices = tts.getProperty('voices')
# # Задать голос по умолчанию
# tts.setProperty('voice', 'ru')
# # Попробовать установить предпочтительный голос
# for voice in voices:
#     ru = voice.id.find('RHVoice\Evgeniy-Eng')  # Найти Анну от RHVoice
#     if ru > -1: # Eсли нашли, выбираем этот голос
#         tts.setProperty('voice', voice.id)
#
# tts.say('Hello world! how are you?')
# tts.runAndWait()

# import pyttsx3
# tts = pyttsx3.init()
# voices = tts.getProperty('voices')
# # Задать голос по умолчанию
# tts.setProperty('voice', 'ru')
# # Попробовать установить предпочтительный голос
# for voice in voices:
#     if voice.name == 'Aleksandr':
#         tts.setProperty('voice', voice.id)
# tts.say('Командный голос вырабатываю, товарищ генерал-полковник!')
# tts.runAndWait()

# import chardet
# about_laung = dict.values(chardet.detect('hello'.encode('cp1251')))  # определение распознаваемого языка
# laung = [*about_laung][2]
# print(laung)

# m = input()
# def insert_context(command):
#     s = command.split()
#     if s[0] == "найди" and (s[1] == "видео" or s[1] == "определение" or s[1] == "перевод" or s[1] == "ютуб"):
#         s = s[1::]
#     elif s[0] == "найди" and s[1] == "в" and (s[2] == "википедии" or s[2] == "ютубе" or s[2] == "google" or s[2] == "гугл"):
#         s = s[2::]
#     new = " ".join(s)
#     return new
# print(insert_context(m))

# m = m.split()
#
# m.pop(0)
# print(m)

from deep_translator import GoogleTranslator
target = input('Введите целевой язык: ')
toTranslate = input('Введите слово для перевода: ')
translated = GoogleTranslator(source='auto', target=target).translate(toTranslate)
print(translated)

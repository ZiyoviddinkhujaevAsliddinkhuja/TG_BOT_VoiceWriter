import os
import telebot
import speech_recognition as sr
import soundfile as sf

token = ''  # <<< Ваш токен

bot = telebot.TeleBot(token)

def oga2wav(filename):
    try:
        new_filename = filename.replace('.oga', '.wav')
        data, samplerate = sf.read(filename)
        sf.write(new_filename, data, samplerate)
        return new_filename
    except Exception as e:
        print(f"Ошибка при конвертации файла {filename} в wav: {e}")
        return None

def recognize_speech(oga_filename):
    try:
        wav_filename = oga2wav(oga_filename)
        if wav_filename is None:
            return "Ошибка при конвертации аудио"

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_filename) as source:
            wav_audio = recognizer.record(source)

        text = recognizer.recognize_google(wav_audio, language='ru')

        if os.path.exists(oga_filename):
            os.remove(oga_filename)
        if os.path.exists(wav_filename):
            os.remove(wav_filename)

        return text
    except Exception as e:
        print(f"Ошибка при распознавании речи: {e}")
        return "Ошибка при распознавании речи"

def download_file(bot, file_id):
    try:
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        filename = file_id + file_info.file_path
        filename = filename.replace('/', '_')
        with open(filename, 'wb') as f:
            f.write(downloaded_file)
        return filename
    except Exception as e:
        print(f"Ошибка при скачивании файла: {e}")
        return None

@bot.message_handler(commands=['start'])
def say_hi(message):
    bot.send_message(message.chat.id, '👋')
    bot.send_message(message.chat.id, 'Привет ' + message.chat.first_name + '!')
    bot.send_message(message.chat.id, 'Бот является переводчиком голосовых сообщений на текстовой формат.')

@bot.message_handler(content_types=['text'])
def helper(message):
    bot.send_message(message.chat.id, 'Отправьте мне голосовое сообщение')


@bot.message_handler(content_types=['voice'])
def transcript(message):
    filename = download_file(bot, message.voice.file_id)
    if filename:
        text = recognize_speech(filename)
    else:
        text = "Ошибка при скачивании файла"
    bot.send_message(message.chat.id, text)

bot.polling()






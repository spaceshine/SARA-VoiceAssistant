from speech_recognition import Microphone, Recognizer

import recognize
import play_speech as speech
import commands
import nlu
import weather

if __name__ == "__main__":
    # инициализация инструментов распознавания речи
    recognizer = Recognizer()
    microphone = Microphone(device_index=1)

    # настройка распознавания
    recognizer.energy_threshold = 4000
    recognizer.pause_threshold = 0.6

    # присваиваем глобальные переменные (чтобы хранить данные)
    recognize.assistant = speech.VoiceAssistant(rate=1.5, voiceid=3)
    recognize.nlu = nlu.NLU()
    commands.weather = weather.SaraWeather()

    # запускаем прослушивание в фоновом режиме
    recognize.listen(microphone, recognizer)

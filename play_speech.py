import json
from playsound import playsound
import win32com.client as wincl


class VoiceAssistant:
    def __init__(self, ttsEngine):
        """
        Настройки голосового ассистента, включающие имя, пол, язык речи
        """
        self.name = ""
        self.sex = ""
        self.speech_language = ""
        self.recognition_language = ""
        self.ttsEngine = ttsEngine
        self.__isrunning = True

    def say(self, text_to_speech):
        """
        Проигрывание речи ответов голосового ассистента (без сохранения аудио)
        :param text_to_speech: текст, который нужно преобразовать в речь
        """
        spk = wincl.Dispatch("SAPI.SpVoice")
        spk.Voice = spk.GetVoices().Item(3)
        spk.Rate = 2
        spk.Speak(text_to_speech)

    @staticmethod
    def say_sound(cat: str, name: str):
        with open("voice.json", "r") as read_file:
            data = json.load(read_file)

        try:
            playsound(f"speech/{data[cat][name]}")
        except KeyError:
            print(f"[err] {cat}; {name}")

    @staticmethod
    def error(number: int):
        with open("voice.json", "r") as read_file:
            data = json.load(read_file)

        try:
            playsound(f"speech/{data['errors'][str(number//10) + '0'][str(number)]}")
        except KeyError:
            print(f"[err] {number}")

    def isrunning(self):
        return self.__isrunning

    def assistant_quit(self):
        self.__isrunning = False


def setup_assistant_voice(assistant):
    """
    Установка голоса по умолчанию (индекс может меняться в
    зависимости от настроек операционной системы)
    :param assistant: объект ассистента
    """
    voices = assistant.ttsEngine.getProperty("voices")

    assistant.recognition_language = "ru-RU"
    # Microsoft Irina Desktop - Russian
    for voice in voices:
        if voice.name == "Tatiana":
            assistant.ttsEngine.setProperty("voice", voice.id)

    rate = assistant.ttsEngine.getProperty('rate')
    assistant.ttsEngine.setProperty('rate', rate - 50)

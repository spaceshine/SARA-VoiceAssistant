import json
from playsound import playsound
import win32com.client as wincl


class VoiceAssistant:
    def __init__(self, rate, voiceid):
        self.__isrunning = True
        self.rate = rate
        self.voiceid = voiceid

    def say(self, text_to_speech):
        """
        Проигрывание речи ответов голосового ассистента (без сохранения аудио)
        :param text_to_speech: текст, который нужно преобразовать в речь
        """
        spk = wincl.Dispatch("SAPI.SpVoice")
        spk.Voice = spk.GetVoices().Item(self.voiceid)
        spk.Rate = self.rate
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

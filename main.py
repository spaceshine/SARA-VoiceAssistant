from speech_recognition import Microphone, Recognizer
import pyttsx3  # синтез речи (Text-To-Speech)
import win32com.client as wincl

import recognize
import play_speech as speech
import commands
import nlu
import weather

if __name__ == "__main__":
    # инициализация инструментов распознавания и ввода речи
    recognizer = Recognizer()
    microphone = Microphone(device_index=1)

    # настройка распознавания
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.6

    nlu = nlu.NLU()
    weather = weather.SaraWeather()

    # настройка данных голосового помощника
    ttsEngine = pyttsx3.init()
    assistant = speech.VoiceAssistant(ttsEngine)
    speech.setup_assistant_voice(assistant)

    recognize.assistant = assistant
    recognize.nlu = nlu
    commands.weather = weather
    recognize.listen_background(microphone, recognizer)

    # while assistant.isrunning():
    #     # старт записи речи с последующим выводом распознанной речи
    #     # и удалением записанного в микрофон аудио
    #     voice_input = recognize.recognize_audio(recognizer, microphone)
    #     print("Voicein:", voice_input)
    #
    #     if voice_input:
    #         for x in commands.assistant_names():
    #             voice_input = voice_input.replace(x, "").strip()
    #         for x in commands.other_words():
    #             voice_input = voice_input.replace(x, "").strip()
    #         voice_input_parts = voice_input.split(" ")
    #
    #         # если было сказано одно слово - выполняем команду сразу без дополнительных аргументов
    #         if len(voice_input_parts) == 1:
    #             intent = commands.get_intent(voice_input, vectorizer, classifier, classifier_probability)
    #             print(intent)
    #             if intent:
    #                 commands.get_commands()["intents"][intent]["responses"](assistant)
    #             else:
    #                 commands.get_commands()["failure_phrases"](assistant)
    #
    #         # в случае длинной фразы - выполняется поиск ключевой фразы и аргументов через каждое слово,
    #         # пока не будет найдено совпадение
    #         if len(voice_input_parts) > 1:
    #             for guess in range(len(voice_input_parts)):
    #                 intent = commands.get_intent((" ".join(voice_input_parts[0:guess])).strip(), vectorizer,
    #                                              classifier, classifier_probability)
    #                 print(intent)
    #                 if intent:
    #                     command_options = [voice_input_parts[guess:len(voice_input_parts)]]
    #                     print(command_options)
    #                     commands.get_commands()["intents"][intent]["responses"](assistant, *command_options)
    #                     break
    #                 if not intent and guess == len(voice_input_parts) - 1:
    #                     commands.get_commands()["failure_phrases"](assistant)

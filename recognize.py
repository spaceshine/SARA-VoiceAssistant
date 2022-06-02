import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import time
import pyfiglet

import commands


def recognize_audio(recognizer, microphone, *args: tuple):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""
        recognizer.adjust_for_ambient_noise(microphone, duration=1)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 10)

        except speech_recognition.WaitTimeoutError:
            print("SARA can't hear you")
            return

        # использование online-распознавания через Google
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет происходит попытка
        # использовать offline-распознавание через Vosk
        except speech_recognition.RequestError:
            print("Internet error")

        return recognized_data


def callback(recognizer, audio):
    try:
        global assistant, nlu
        voice_input = recognizer.recognize_google(audio, language="ru-RU").lower()

        print("Callback:", voice_input)

        if voice_input:
            for x in commands.assistant_names():
                voice_input = voice_input.replace(x, "").strip()
            for x in commands.other_words():
                voice_input = voice_input.replace(x, "").strip()
            voice_input_parts = voice_input.split(" ")

            # если было сказано одно слово - выполняем команду сразу без дополнительных аргументов
            if len(voice_input_parts) == 1:
                intent = commands.get_intent(voice_input,
                                             nlu.vectorizer, nlu.classifier, nlu.classifier_probability)
                print(intent)
                if intent:
                    commands.get_commands()["intents"][intent]["responses"](assistant)
                else:
                    commands.get_commands()["failure_phrases"](assistant)

            # в случае длинной фразы - выполняется поиск ключевой фразы и аргументов через каждое слово,
            # пока не будет найдено совпадение
            if len(voice_input_parts) > 1:
                for guess in range(len(voice_input_parts)):
                    intent = commands.get_intent((" ".join(voice_input_parts[0:guess])).strip(),
                                                 nlu.vectorizer, nlu.classifier, nlu.classifier_probability)
                    print(intent)
                    if intent:
                        command_options = [voice_input_parts[guess:len(voice_input_parts)]]
                        print(command_options)
                        commands.get_commands()["intents"][intent]["responses"](assistant, *command_options)
                        break
                    if not intent and guess == len(voice_input_parts) - 1:
                        commands.get_commands()["failure_phrases"](assistant)

    except speech_recognition.UnknownValueError:
        print("[log] Голос не распознан!")
    except speech_recognition.RequestError:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def listen_background(microphone, recognizer):
    global assistant
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    recognizer.listen_in_background(microphone, callback)

    pyfiglet.print_figlet("SARA  v 0. 1. 1", font='slant')
    while assistant.isrunning():
        time.sleep(0.1)

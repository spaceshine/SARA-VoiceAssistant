import datetime as dt
import subprocess
import win32con
import win32gui
from pynput.keyboard import Controller, Key

import search
import voice_timers


def assistant_names():
    return \
        tuple(("сара", "сар", "с. а."))


def other_words():
    return \
        tuple(("пожалуйста", "прошу тебя", "прошу", "ага", " а ", "мне",
               "спасибо"))


def get_commands():
    return \
        {
            "intents": {
                "hello": {
                    "examples": ["привет", "доброе утро"],
                    "responses": play_greetings
                },
                "goodbye": {
                    "examples": ["пока", "выключись"],
                    "responses": play_quit
                },
                "google-search": {
                    "examples": ["загугли", "найди"],
                    "responses": search.search_google
                },
                "wikipedia-search": {
                    "examples": ["найди в википедии", "википедия"],
                    "responses": search.search_wiki
                },
                "weather_forecast": {
                    "examples": ["прогноз погоды", "погода"],
                    "responses": get_weather_forecast
                },
                "open-application": {
                    "examples": ["открой", "запусти"],
                    "responses": open_application
                },
                "minimize-window": {
                    "examples": ["сверни", "сверни окно"],
                    "responses": minimize_window
                },
                "maximize-window": {
                    "examples": ["обратно", "разверни окно"],
                    "responses": maximize_window
                },
                "close-window": {
                    "examples": ["закрой", "закрой окно"],
                    "responses": close_window
                },
                "pause-play": {
                    "examples": ["пауза", "давай дальше", "стоп"],
                    "responses": pause_play
                },
                "countdown": {
                    "examples": ["считай", "отчёт", "обратный"],
                    "responses": start_countdown
                },
                "timer": {
                    "examples": ["таймер", "засеки"],
                    "responses": voice_timers.timer
                }
            },
            "failure_phrases": not_find
        }


def prepare_corpus(vectorizer, classifier, classifier_probability):
    """
    Подготовка модели для угадывания намерения пользователя
    """
    corpus = []
    target_vector = []
    for intent_name, intent_data in get_commands()["intents"].items():
        for example in intent_data["examples"]:
            corpus.append(example)
            target_vector.append(intent_name)

    training_vector = vectorizer.fit_transform(corpus)
    classifier_probability.fit(training_vector, target_vector)
    classifier.fit(training_vector, target_vector)


def get_intent(request, vectorizer, classifier, classifier_probability):
    """
    Получение наиболее вероятного намерения в зависимости от запроса пользователя
    :param classifier_probability:
    :param classifier:
    :param vectorizer:
    :param request: запрос пользователя
    :return: наиболее вероятное намерение
    """
    best_intent = classifier.predict(vectorizer.transform([request]))[0]

    index_of_best_intent = list(classifier_probability.classes_).index(best_intent)
    probabilities = classifier_probability.predict_proba(vectorizer.transform([request]))[0]

    best_intent_probability = probabilities[index_of_best_intent]

    # при добавлении новых намерений стоит уменьшать этот показатель
    if best_intent_probability > 0.150:
        return best_intent


def execute_command_with_name(assistant, command_name: str, *args: list):
    """
    Выполнение заданной пользователем команды с дополнительными аргументами
    :param assistant: объект ассистента
    :param command_name: название команды
    :param args: аргументы, которые будут переданы в функцию
    :return:
    """
    commands = get_commands()
    isfound = False
    for key in commands.keys():
        if command_name in key:
            commands[key](assistant, *args)
            isfound = True

    if not isfound:
        assistant.error(44)
        assistant.say(f"{command_name}")


def play_greetings(assistant, *args: tuple):
    now = dt.datetime.now()
    if 4 < now.hour <= 12:
        assistant.say_sound("hello", "morning")
    elif 12 < now.hour <= 16:
        assistant.say_sound("hello", "day")
    elif 16 < now.hour <= 24:
        assistant.say_sound("hello", "evening")
    elif 0 <= now.hour <= 4:
        assistant.say_sound("hello", "night")
    else:
        assistant.say_sound("hello", "default")


def play_quit(assistant, *args: tuple):
    now = dt.datetime.now()
    if 4 < now.hour <= 12:
        assistant.say_sound("goodbye", "morning")
    elif 12 < now.hour <= 16:
        assistant.say_sound("goodbye", "day")
    elif 16 < now.hour <= 24:
        assistant.say_sound("goodbye", "evening")
    elif 0 <= now.hour <= 4:
        assistant.say_sound("goodbye", "night")
    else:
        assistant.say_sound("goodbye", "default")
    assistant.assistant_quit()


def say_thanks(assistant, *args: tuple):
    assistant.say_sound('other', 'thanks')
    # text = ' '.join(*args)
    # if text not in ('', ' '):
    #     command, command_options = command_from_text(text)
    #     execute_command_with_name(assistant, command, command_options)


def not_find(assistant, *args: tuple):
    pass  # assistant.say_sound('other', 'notfind')


def list_in_list(a: tuple, b: tuple) -> bool:
    for i in a:
        if i in b:
            return True
    return False


def get_weather_forecast(assistant, *args: tuple):
    global weather
    if list_in_list(("сегодня", "сейчас"), args[0]):
        assistant.say(weather.today())
    elif list_in_list(("завтра", "ближайшие", "ближайший", "ближайшая", "ближайшую"), args[0]):
        assistant.say(weather.closest())


def open_application(assistant, *args: tuple):
    if list_in_list(("telegram", "телеграм", "телеграмм", "тг"), args[0]):
        subprocess.Popen('"C:\\Users\\space\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe"')
        assistant.say_sound('applications', 'telegram')
    elif list_in_list(("spotify", "спотифай"), args[0]):
        subprocess.Popen('"C:\\Users\\space\\AppData\\Roaming\\Spotify\\Spotify.exe"')
        assistant.say_sound('applications', 'spotify')
    elif list_in_list(("блокнот", "текстовик"), args[0]):
        subprocess.Popen('"C:\\Windows\\System32\\notepad.exe"')
        assistant.say_sound('applications', 'notepad')
    elif list_in_list(("calculator", "калькулятор"), args[0]):
        subprocess.Popen('"C:\\Windows\\System32\\calc.exe"')
        assistant.say_sound('applications', 'calc')
    elif list_in_list(("discord", "дискорд", "дс"), args[0]):
        subprocess.run('C:\\Users\\space\\AppData\\Local\\Discord\\Update.exe --processStart Discord.exe', shell=True)
        assistant.say_sound('applications', 'discord')
    elif list_in_list(("docs", "документ", "документы", "докс"), args[0]):
        search.open_docs(assistant)


def minimize_window(assistant, *args: tuple):
    win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_MINIMIZE)


def maximize_window(assistant, *args: tuple):
    win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_NORMAL)


def close_window(assistant, *args: tuple):
    win32gui.PostMessage(win32gui.GetForegroundWindow(), win32con.WM_CLOSE, 0, 0)


def pause_play(assistant, *args: tuple):
    kb = Controller()
    with kb.pressed(Key.cmd, Key.ctrl_l, Key.shift, Key.f24):
        kb.release(Key.f24)
        kb.release(Key.shift)
        kb.release(Key.ctrl_l)
        kb.release(Key.cmd)


def start_countdown(assistant, *args: tuple):
    # TODO: сделать разные start`ы;
    # TODO: На данном этапе это будет неэффективно, тк распознавание будет работать "через раз".
    voice_timers.countdown(assistant, start=10)

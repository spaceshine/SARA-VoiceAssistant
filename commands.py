import datetime as dt

import search


def assistant_names():
    return \
        tuple(("сара", "сар", "с. а."))


def other_words():
    return \
        tuple(("пожалуйста", "прошу тебя", "прошу", "ага", " а ", "мне"))


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
                "youtube-search": {
                    "examples": ["видео", "найди видео"],
                    "responses": search_youtube
                },
                "wikipedia-search": {
                    "examples": ["найди на википедии", "википедия"],
                    "responses": search.search_wiki
                },
                "weather_forecast": {
                    "examples": ["прогноз погоды", "какая погода",
                                 "погода"],
                    "responses": get_weather_forecast
                },
                "translation": {
                    "examples": ["выполни перевод", "переведи",
                                 "перевод"],
                    "responses": text_translate
                },
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
    if best_intent_probability > 0.157:
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
    pass


def search_youtube(assistant, *args: tuple):
    pass


def text_translate(assistant, *args: tuple):
    pass


def list_in_list(a: tuple, b: tuple) -> bool:
    for i in a:
        if i in b:
            return True
    return False


def get_weather_forecast(assistant, *args: tuple):
    global weather
    if list_in_list(("сегодня", "сейчас"), args[0]):
        assistant.say(weather.today())
    elif list_in_list(("завтра", "ближайшие", "ближайший"), args[0]):
        assistant.say(weather.closest())

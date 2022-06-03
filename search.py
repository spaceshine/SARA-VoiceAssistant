import webbrowser
import wikipediaapi  # поиск определений в Wikipedia


def search_google(assistant, *args: tuple):
    if not args:
        assistant.error(54)
        return

    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    webbrowser.register('google-chrome', None, webbrowser.BackgroundBrowser(chrome_path))

    new_tab = webbrowser.get(using='google-chrome').open_new_tab(f"google.com/search?q={'+'.join(*args)}")

    if new_tab is None:
        assistant.error(54)
    else:
        assistant.say_sound("search", "google")


def crop_definition(text: str):
    return text[:text.find('(')] + text[text.find(')'):]


def search_wiki(assistant, *args: tuple):
    if not args:
        assistant.error(54)
        return

    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    webbrowser.register('google-chrome', None, webbrowser.BackgroundBrowser(chrome_path))

    search_term = " ".join(args[0])

    # установка языка
    wiki = wikipediaapi.Wikipedia('ru')

    # поиск страницы по запросу, чтение summary, открытие ссылки на страницу для получения подробной информации
    wiki_page = wiki.page(search_term)
    # try:
    if wiki_page.exists():
        assistant.say_sound('search', 'wiki')
        webbrowser.get('google-chrome').open(wiki_page.fullurl)

        # чтение ассистентом первых двух предложений summary со страницы Wikipedia
        assistant.say(crop_definition(wiki_page.summary).split(".")[:2])
    else:
        # открытие ссылки на поисковик в браузере в случае, если на Wikipedia не удалось найти ничего по запросу
        assistant.say_sound('search', 'wiki-not-find')
        search_google(assistant, *args)

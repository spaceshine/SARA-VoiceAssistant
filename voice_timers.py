from threading import Timer


class CountdownTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def countdown(assistant, start=10, *args: tuple):
    countdown_tick.counter = start
    # 0.5 - поправка на отклик
    countdown_tick.timer = CountdownTimer(0.5, countdown_tick, args=(assistant, ))
    countdown_tick.timer.start()


def countdown_tick(assistant, *args: tuple):
    if countdown_tick.counter <= 0:
        countdown_tick.timer.cancel()
    assistant.say_sound("countdown", str(countdown_tick.counter))
    countdown_tick.counter -= 1


def timer_end(assistant):
    assistant.say_sound("timer", "end")


def timer(assistant, *args: tuple):
    if args is None:
        return
    for word in args[0]:
        if word in ("одну", ):
            word = '1'
        if word.isdigit():
            t = Timer(float(word)*60, timer_end, args=(assistant,))
            t.start()
            assistant.say(f"Засекаю {'одну' if word=='1' else ('две' if word=='2' else word)} {'минуту' if int(word)%10 == 1 else ('минуты' if 1<int(word)%10<5 else 'минут')}")
            return


countdown_tick.counter = None
countdown_tick.timer = None

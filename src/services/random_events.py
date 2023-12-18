import typing
import random

from db.models import Hedgehog
from db.func import DB


class EventAnswer:

    def __init__(
            self,
            stop: bool,
            text: str
    ):
        self.stop = stop
        self.text = text


class RandomEvents:
    def __init__(self):
        self.events: list[typing.Coroutine] = []

    async def get(self, hedgehog: Hedgehog):
        """выполняет случайноее действие"""
        if random.randint(1, 8) == 3:  # basic event
            event = random.choice(self.events)
            ans: EventAnswer = await event(hedgehog)
            return ans
        if random.randint(1, 15) == 3:  # goiden apple
            ans: EventAnswer = await golden_apple(hedgehog)
            return ans

    def set(self):
        def decorator(coroutine: typing.Coroutine):
            self.events.append(coroutine)
            return coroutine
        return decorator


work = RandomEvents()
eat = RandomEvents()


# goiden apple
async def golden_apple(hedgehog: Hedgehog):

    text = random.choice(
        [
            "По пути он увидел необычное блестящее яблочко.",
            "Он нашёл красивое золотое яблочко, что же это такое?",
            "вместе с обычными он получил одно золотое яблочко."
        ]
    )

    upped_mood = DB.hedgehog.up_mood(+4, hedgehog=hedgehog)
    hedgehog.golden_apples += 1
    hedgehog.save()
    text = f"{text}\n\nНастроение: +{upped_mood}{'(Максимальное)' if upped_mood == 0 else ''}\nЗолотые яблочки: +1"
    return EventAnswer(False, text)

# ==================BASIC EVENTS================


# bad events
@eat.set()
async def choked(hedgehog: Hedgehog):

    text = random.choice(
        [
            "Ваш ёжик подавился и не смог поесть.",
            "О нет, ваш ёжик подавился и очень расстроился.",
            "Эта еда слишком острая, ёжик подавился и теперь не может успокоиться.",
            "Ёжик подавился и отказывается есть дальше.",
            "Кажется, ёжик подавился куском еды, и теперь он весь в слезах.",
            "Ваш ёжик подавился и не может отойти от происшествия."
        ]
    )

    upped_mood = DB.hedgehog.up_mood(-2, hedgehog=hedgehog)
    text = f"{text}\n\nНастроение: {upped_mood}"
    return EventAnswer(True, text)


@work.set()
async def tired(hedgehog: Hedgehog):

    text = random.choice(
        [
            "Он очень сильно устал.",
            "На него накричал начальник."
        ]
    )

    upped_mood = DB.hedgehog.up_mood(-2, hedgehog=hedgehog)
    text = f"{text}\n\nНастроение: {upped_mood}"
    return EventAnswer(False, text)


# good events
@eat.set()
async def liked(hedgehog: Hedgehog):

    text = random.choice(
        [
            "Сегодня вашему ёжику всё особенно понравилось.",
            "Ёжик ел с большим аппетитом, ему всё очень понравилось.",
            "Ёжику явно по вкусу была эта еда, он ел с таким удовольствием.",
            "С лакомством ёжик наедался - ему явно понравилось.",
            "Еда была угощение на вкус ёжику - он не мог наесться.",
            "Видно, что ёжику не хватило этой вкусной еды, он вылизывал тарелку досуха.",
            "Ёжику пришлась по вкусу эта деликатесная трапеза - он наслаждался каждым кусочком.",
            "По его довольному храпению можно было понять, что еда пришлась по вкусу.",
            "Все остальное в этом мире перестало существовать, когда ёжик погрузился в еду, которая ему безумно понравилась.",
            "Ёжик облизывал свои усы с таким наслаждением после трапезы, что было ясно - он был очень доволен едой.",
            "Морда ёжика была усыпана крошками - он явно был в восторге от этой еды.",
            "После того, как ёжик закончил есть, он приступил к чистке лапок с видом удовлетворения, словно хотел сохранить запах этой вкуснейшей пищи как можно дольше."
        ]
    )

    upped_mood = DB.hedgehog.up_mood(+5, hedgehog=hedgehog)
    text = f"{text}\n\nНастроение: +{upped_mood}{'(Максимальное)' if upped_mood == 0 else ''}\nСытость: +1"
    return EventAnswer(True, text)


@work.set()
async def praised(hedgehog: Hedgehog):

    text = random.choice(
        [
            "Его похвалили и он очень этому рад.",
            "Его проект понравился начальнику",
        ]
    )

    upped_mood = DB.hedgehog.up_mood(+6, hedgehog=hedgehog)
    text = f"{text}\n\nНастроение: +{upped_mood}{'(Максимальное)' if upped_mood == 0 else ''}"
    return EventAnswer(False, text)


class Events:
    work = work
    eat = eat

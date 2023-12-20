from vkbottle import LoopWrapper


def gen_list(lst: list, num: int):
    """генерация списков с вложенными списками определённой длины"""
    for i in range((len(lst) + num-1) // num):
        yield lst[i*num:(i+1)*num]


def load_tasks(lw: LoopWrapper, *tasks):
    for task in tasks:
        lw.add_task(task)

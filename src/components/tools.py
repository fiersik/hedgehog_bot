def gen_list(lst: list, num: int):
    """генерация списков с вложенными списками определённой длины"""
    for i in range((len(lst) + num-1) // num):
        yield lst[i*num:(i+1)*num]

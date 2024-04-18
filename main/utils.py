import random


def get_random_choice(object_list):
    """
    Функция для получения 3х случайных объектов.
    """
    if object_list and len(object_list) >= 3:
        random_list = []
        while len(random_list) < 3:
            random_item = random.choice(object_list)
            if random_item not in random_list:
                random_list.append(random_item)

        return random_list

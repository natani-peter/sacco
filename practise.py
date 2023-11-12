import json


def get_number():
    favourite_number = input('What is your favourite number: ')

    with open('number.json', 'w') as file:
        json.dump(favourite_number, file)
        print(f"Your favourite number is {favourite_number}")


def read_number():
    try:
        with open('number.json') as file:
            number = json.load(file)
    except FileNotFoundError:
        return None

    return number


def guess():

    number = read_number()

    if number:
        print(f'I know your favourite number, it\'s {number}')
    else:
        get_number()
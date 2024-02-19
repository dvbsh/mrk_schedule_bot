from bot import bot
from aiogram.enums.parse_mode import ParseMode
from .lessons_message import lessons
from config import chat_id
import json


def get_followed_users():
    try:
        with open('data.json', 'r') as file:
            users_dict = json.load(file)
            if users := users_dict.get('followed'):
                return [i for i in users.split(',')]
        with open('data.json', 'w') as file:
            users_dict.update({'followed': ""})
            file.write(json.dumps(users_dict, indent=4))
            return []
    except Exception as e:
        return {'error': e}


def add_followed_user(username):
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            users = data['followed']
        if users and username not in users:
            data.update({'followed': ((users + "," if users else '') + f"{username}")})
            with open('data.json', 'w') as file:
                file.write(json.dumps(data, indent=4))
        elif not users:
            data.update({'followed': f",{username}"})
            with open('data.json', 'w') as file:
                file.write(json.dumps(data, indent=4))
        return None
    except TypeError:
        return 'Ошибка: не удалось найти username (тег) пользователя.'


def remove_followed_user(username):
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            users = data['followed']
        if users and username in users:
            data.update({'followed': users.replace(f"{username},", '')})
            with open('data.json', 'w') as file:
                file.write(json.dumps(data, indent=4))
    except Exception as e:
        print(e)


async def warn():
    users = get_followed_users()
    if not isinstance(users, dict):
        mention = " ".join(["@" + username for username in users])
        await bot.send_message(chat_id=chat_id, text=f'{mention}\n\n{lessons()}', parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    else:
        await bot.send_message(chat_id=chat_id, text=f'Ошибка: {users["error"]}')

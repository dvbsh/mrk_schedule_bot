from aiogram import Dispatcher, F
from aiogram.enums import ChatType
from aiogram.filters import Command, or_f, ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatMemberUpdated
from aiogram.enums.parse_mode import ParseMode
from tools.lessons_message import lessons
from tools.misc import get_followed_users, add_followed_user, remove_followed_user, warn
from config import admins, welcome_text

dp = Dispatcher()


@dp.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION), F.chat.type.in_({ChatType.SUPERGROUP, ChatType.GROUP}))
async def welcome(event: ChatMemberUpdated):
    return event.answer(welcome_text, parse_mode=ParseMode.MARKDOWN_V2)


@dp.message(Command('help'))
async def bot_help(msg: Message):
    await msg.answer(welcome_text, parse_mode=ParseMode.MARKDOWN_V2)


@dp.message(or_f(Command('start', 'schedule', 'sch', 'расписание', 'пара', 'расп')))
async def start(msg: Message):
    if (msg.chat.type in ['group', 'supergroup'] and msg.text != '/start') or (msg.chat.type == 'private'):
        await msg.reply(lessons(), parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='👀 Отслеживать начало пары', callback_data='follow')] if msg.from_user.username not in get_followed_users() else [InlineKeyboardButton(text='❌ Прекратить отслеживание', callback_data='unfollow')]]) if msg.chat.type == 'private' else None, disable_web_page_preview=True)


@dp.message(or_f(Command('follow', 'unfollow')))
async def command_follow_notifications(msg: Message):
    users = get_followed_users()
    username = msg.from_user.username
    name = msg.from_user.first_name
    if '/follow' in msg.text:
        if users and username in users:
            await msg.reply(f'{name}, Вы уже подписаны на оповещение.')
        else:
            result = add_followed_user(username)
            if not result:
                if msg.chat.type != 'private':
                    text = f'{name} подписался(-ась) на оповещение перед началом пары!'
                elif msg.chat.type == 'private':
                    text = f'{name}, Вы успешно подписались на оповещение!'
            else:
                text = result
            await msg.reply(text)
    else:
        if users and username in users:
            remove_followed_user(username)
            await msg.reply(f'{name}, Вы отписались от оповещения.')
        else:
            await msg.reply(f'{name}, Вы не подписаны на оповещение!')


@dp.callback_query(F.data.in_({'follow', 'unfollow'}))
async def command_follow_notifications(callback: CallbackQuery):
    users = get_followed_users()
    username = callback.from_user.username
    name = callback.from_user.first_name
    if callback.data == 'follow':
        if users and username in users:
            await callback.message.answer(f'{name}, Вы уже подписаны на оповещение.')
        else:
            add_followed_user(username)
            await callback.message.answer(f'{name}, Вы успешно подписались на оповещение!')
    else:
        if users and username in users:
            remove_followed_user(username)
            await callback.message.answer(f'{name}, Вы отписались от оповещения.')
        else:
            await callback.message.answer(f'{name}, Вы не подписаны на оповещение!')
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='👀 Отслеживать начало пары', callback_data='follow')] if callback.from_user.username not in get_followed_users() else [InlineKeyboardButton(text='❌ Прекратить отслеживание', callback_data='unfollow')],]))
    await callback.answer()


@dp.message(Command('warn'))
async def warn_all(msg: Message):
    if msg.from_user.id in admins:
        await warn()
    else:
        await msg.reply('У вас недостаточно прав, чтобы использовать данную команду.')

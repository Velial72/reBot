import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ContentType
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import User, CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Column, Start
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput
from aiogram_dialog.widgets.media import StaticMedia
from environs import Env

from tools.LEXICON import LEXICON
from tools.functions import message_send_photo, callback_send_photo

from dialogs.create_game import CreateGameSG
from dialogs.payment import PaymentSG
from dialogs.my_groups import GroupSG

player_data = {
    'player_id': 123,
    'game': True,
    'registration_on_game': True,
    'name': 'Anton',
    'email': 'a@a.ru',
    'wish': 'car'
}


class AdminSG(StatesGroup):
    start = State()


async def get_name(event_from_user: User, **kwargs):
    return {'name': event_from_user.username or 'Путник', "extended": True}


start_dialog = Dialog(
    Window(
        Format('{name}, что тебя интересует?'),
        Column(
            Start(
                text=Format(f'{LEXICON["create_group"]}'),
                id='create_group',
                state=CreateGameSG.start),
            Start(
                text=Format(f'{LEXICON["my_groups.py"]}'),
                id='my_groups.py',
                state=GroupSG.start,
                when=F["extended"],
            ),
            Start(
                text=Format(f'{LEXICON["payment"]}'),
                id='payment',
                state=PaymentSG.start),
        ),
        getter=get_name,
        state=AdminSG.start,

    ),

)

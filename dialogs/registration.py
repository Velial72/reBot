import importlib
from datetime import date

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import User, CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.kbd import Row, Start, SwitchTo
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput
from aiogram_dialog.widgets.media import StaticMedia
from aiogram.utils.deep_linking import create_start_link
from environs import Env

from dialogs.start_module import AdminSG
from tools.LEXICON import LEXICON

player_data = {
    'player_id': 123,
    'game': True,
    'registration_on_game': True,
    'name': 'Anton',
    'email': 'a@a.ru',
    'wish': 'car'
}


class RegistrationSG(StatesGroup):
    name = State()
    email = State()
    wish = State()
    confirm = State()
    change = State()
    rename = State()
    finish = State()


async def get_user_name(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    player_data['name'] = message.text
    print(player_data)
    await dialog_manager.next()


async def get_email(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    player_data['email'] = message.text
    print(player_data)
    await dialog_manager.next()


async def get_wish(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    player_data['wish'] = message.text
    print(player_data)
    await dialog_manager.next()


async def get_items(**kwargs):
    return {'items': (
        ('Имя', player_data['name']),
        ('email', player_data['email']),
        ('Желание', player_data['wish']),
    )}


registration_dialog = Dialog(
    Window(
        Const(f'{LEXICON["user_name"]}'),
        TextInput(
            id='player_name',
            on_success=get_user_name
        ),
        state=RegistrationSG.name
    ),
    Window(
        Const(f'{LEXICON["email"]}'),
        TextInput(
            id='email',
            on_success=get_email
        ),
        state=RegistrationSG.email
    ),
    Window(
        StaticMedia(
            path='media/present.jpg',
            type=ContentType.PHOTO
        ),
        Const(f'{LEXICON["wishlist"]}'),
        TextInput(
            id='wishlist',
            on_success=get_wish
        ),
        state=RegistrationSG.wish
    ),
    Window(
        Const('Проверь, все ли корректно'),
        List(field=Format('{item[0]}. {item[1]}'),
             items='items'),
        Row(
            SwitchTo(
                Const('Все отлично!'),
                id='confirm',
                state=RegistrationSG.finish
            ),
            SwitchTo(
                Const('Исправить'),
                id='change_registration',
                state=RegistrationSG.change
            )
        ),
        getter=get_items,
        state=RegistrationSG.confirm
    ),
    #Window(),
    Window(
        StaticMedia(
            path='media/firework.jpg',
            type=ContentType.PHOTO
        ),
        Const('Превосходно, ты в игре!\n Жми кнопку'),
        Start(
            Const('На главную'),
            id='go_start',
            state=AdminSG.start,
            mode=StartMode.RESET_STACK
        ),
        state=RegistrationSG.finish
    )
)

import importlib
from datetime import date

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import User, CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Next
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput
from aiogram_dialog.widgets.media import StaticMedia
from aiogram.utils.deep_linking import create_start_link
from environs import Env

from tools.LEXICON import LEXICON
import pprint

group_data = {
    'xsf': {
        'admin_id': 1,
        'group_name': 'Умные Хомяки',
        'description': 'test',
        'price': '1000',
        'link': 'https://t.me/ted23_bot?start=123',
        'wish': 'car'
    },
    'sfd': {
        'admin_id': 0,
        'group_name': 'Горячие головы',
        'description': 'qwerty',
        'price': '5000',
        'link': 'https://t.me/ted23_bot?start=123',
        'wish': 'airplane'
    },
    'Yellow_tree': {
        'admin_id': 0,
        'group_name': 'Yellow tree',
        'description': 'Green tree',
        'price': '4500',
        'link': 'https://t.me/ted23_bot?start=123',
        'wish': 'airplane'
    },
    'Justice_league': {
        'admin_id': 1,
        'group_name': 'Justice league',
        'description': 'Я - Бэтмен',
        'price': '3000',
        'link': 'https://t.me/ted23_bot?start=123',
        'wish': 'airplane'
    }
}


class GroupSG(StatesGroup):
    start = State()
    chosen_group = State()


async def get_group_data(dialog_manager: DialogManager,**kwargs):
    pprint.pprint(dialog_manager.start_data)
    return {'group_name': 'test', 'description': 'test 2', 'link': 'test 3'}


def group_btn_creator(btn):
    buttons = []
    for group in btn.keys():
        buttons.append(Next(Const(group), id=group))
    return buttons


group_btn = group_btn_creator(group_data)

my_group_dialog = Dialog(
    Window(
        Const('Вот твои группы'),
        ScrollingGroup(
            *group_btn,
            id="my_groups",
            width=1,
            height=2
        ),
        state=GroupSG.start
    ),
    Window(
        Format('Группа {group_name}\n{description}\nСсылка для приглашения участников: {link}'),
        getter=get_group_data,
        state=GroupSG.chosen_group
    )
)

import importlib
from datetime import date

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import User, CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select, SwitchTo, Back
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput
from aiogram_dialog.widgets.media import StaticMedia
from aiogram.utils.deep_linking import create_start_link
from environs import Env

from tools.LEXICON import LEXICON
import pprint

group_data = {
    'xsf': {
        'admin_id': True,
        'group_name': 'Умные Хомяки',
        'description': 'test',
        'price': '1000',
        'link': 'https://t.me/ted23_bot?start=123',
        'wish': 'car'
    },
    'sfd': {
        'admin_id': False,
        'group_name': 'Горячие головы',
        'description': 'qwerty',
        'price': '5000',
        'link': 'https://t.me/ted23_bot?start=123',
        'wish': 'airplane'
    },
    'Yellow_tree': {
        'admin_id': False,
        'group_name': 'Yellow tree',
        'description': 'Green tree',
        'price': '4500',
        'link': 'https://t.me/ted23_bot?start=123',
        'wish': 'airplane'
    },
    'Justice_league': {
        'admin_id': True,
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
    group_info = State()
    admin_group = State()


async def group_btn_creator(**kwargs):
    buttons = []
    for group_id, group_name in group_data.items():
        btn = (group_name['group_name'], group_id)
        buttons.append(btn)
    return {'buttons': buttons}


async def get_group_data(callback: CallbackQuery, button: Button,
                         dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['group_name'] = item_id
    await dialog_manager.next()


async def get_group_name(dialog_manager: DialogManager, **kwargs):
    group = dialog_manager.dialog_data['group_name']
    return {
        'group_name': group_data[group]['group_name'],
        'description': group_data[group]['description'],
        'link': group_data[group]['link'],
        'admin_id': group_data[group]['admin_id']
    }


my_group_dialog = Dialog(
    Window(
        Const('Вот твои группы'),
        ScrollingGroup(
            Select(
                Format('{item[0]}'),
                id='on_group',
                item_id_getter=lambda x: x[1],
                items='buttons',
                on_click=get_group_data
            ),
            id='scroll_groups',
            width=2,
            height=1
        ),
        state=GroupSG.start,
        getter=group_btn_creator
    ),
    Window(
        Format('Группа {group_name}\n{description}'),
        Format('Ссылка для приглашения участников: {link}', when='admin_id'),
        SwitchTo(Const('Управлять группой'), id='admin_group', state=GroupSG.admin_group, when='admin_id'),
        Back(Const('Назад'),id='step_back'),
        getter=get_group_name,
        state=GroupSG.chosen_group
    ),
    # Window(
    #
    # )
)

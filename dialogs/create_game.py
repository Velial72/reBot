import importlib
from datetime import date

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import User, CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row, Group, Calendar, Select
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput
from aiogram_dialog.widgets.media import StaticMedia
from aiogram.utils.deep_linking import create_start_link
from environs import Env

from tools.LEXICON import LEXICON


env = Env()
env.read_env()

BOT_TOKEN = env('TELEGRAM_TOKEN')

bot = Bot(token=BOT_TOKEN)


group_data = {
    'admin_id': 12345,
    'game_id': 986532,
    'group_name': '1',
    'description': '',
    'information_date': None,
    'game_date': None,
    'price': '',
    'link': '',

}


class CreateGameSG(StatesGroup):
    start = State()
    description = State()
    date_of_information = State()
    date_of_game = State()
    choose_price = State()
    link = State()


async def go_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.back()


async def go_start(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    module = importlib.import_module("dialogs.start_module")
    await dialog_manager.start(state=module.AdminSG.start, mode=StartMode.RESET_STACK)


async def choose_group_name(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    group_data['group_name'] = message.text
    print(group_data)
    await dialog_manager.next()


async def choose_group_description(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    group_data['group_description'] = message.text
    print(group_data)
    await dialog_manager.next()


async def on_information_date_selected(callback: CallbackQuery, widget,
                                       dialog_manager: DialogManager, selected_date: date):
    group_data['information_date'] = str(selected_date)
    print(group_data)
    print(str(selected_date))
    print(type(selected_date))
    await dialog_manager.next()


async def on_game_date_selected(callback: CallbackQuery, widget,
                                dialog_manager: DialogManager, selected_date: date):
    group_data['game_date'] = str(selected_date)
    print(group_data)
    print(str(selected_date))
    print(type(selected_date))
    await dialog_manager.next()


async def on_price_selected(callback: CallbackQuery, widget: Select,
                            dialog_manager: DialogManager, item_id: str):
    group_data['price'] = item_id
    print(group_data)
    await dialog_manager.next()


async def get_price(**kwargs):
    price = [
        ('1000 - 1500 руб.', '1000 - 1500 руб.'),
        ('1500 - 3000 руб.', '1500 - 3000 руб.'),
        ('3000 - 5000 руб.', '3000 - 5000 руб.'),
        ('Больше 5000 руб.', 'Больше 5000 руб.'),
    ]
    return {'price': price}


async def get_link(**kwargs):
    link = await create_start_link(bot=bot, payload='123')
    return {'link': link}


create_game_dialog = Dialog(
    Window(
        Const(text="Самое время создать новую группу, куда ты можешь пригласить своих друзей, коллег или "
                   "родственников\n\nДавай выберем забавное имя для новой группы!"),
        TextInput(
            id='group_name',
            on_success=choose_group_name
        ),
        state=CreateGameSG.start
    ),
    Window(
        Const(
            text="Классное название!\n\nА теперь напиши мне короткое описание вашей группы. Его будут видеть "
                 "участники при"
                 "регистрации и на странице группы."),
        TextInput(
            id='group_description',
            on_success=choose_group_description,
        ),
        Row(
            Button(
                Const('Изменить название'),
                id='b_back',
                on_click=go_back
            ),
            Button(
                Const('Ну нахер!'),
                id='home',
                on_click=go_start
            ),
        ),
        state=CreateGameSG.description
    ),
    Window(
        StaticMedia(
            path='media/firework.jpg',
            type=ContentType.PHOTO
        ),
        Format(
            text=f"{LEXICON['santa_selection_date']}"),
        Calendar(id='information_date', on_click=on_information_date_selected),
        Row(
            Button(
                Const('Изменить описание'),
                id='b_back',
                on_click=go_back
            ),
            Button(
                Const('Ну нахер!'),
                id='home',
                on_click=go_start
            )
        ),
        state=CreateGameSG.date_of_information
    ),
    Window(
        Const("Теперь все понятно!\n\nПора указать дату и время проведения розыгрыша, чтобы бот уведомил участников."),
        Calendar(id='game_date', on_click=on_game_date_selected),
        Row(
            Button(
                Const('Изменить дату'),
                id='b_back',
                on_click=go_back
            ),
            Button(
                Const('Ну нахер!'),
                id='home',
                on_click=go_start
            )
        ),
        state=CreateGameSG.date_of_game
    ),
    Window(
        StaticMedia(
            path='media/present2.jpg',
            type=ContentType.PHOTO
        ),
        Const('Выбери стоимость подарка'),
        Group(
            Select(
                Format('{item[0]}'),
                id='categ',
                item_id_getter=lambda x: x[1],
                items='price',
                on_click=on_price_selected,
            ),
            width=2
        ),
        Row(
            Button(
                Const('Изменить дату розыгрыша'),
                id='b_back',
                on_click=go_back
            ),
            Button(
                Const('Ну нахер!'),
                id='home',
                on_click=go_start
            )
        ),
        state=CreateGameSG.choose_price,
        getter=get_price
    ),
    Window(
        Format(f'Игра создана!\nНазвание: {group_data["group_name"]}\nОписание группы: {group_data["description"]}\n'
               f'Жеребьевка состоится: {group_data["information_date"]}\nДата игры: {group_data["game_date"]}\nЦена '
               f'подарка: {group_data["price"]}\n'),
        Format('Ссылка: {link}'),
        getter=get_link,
        state=CreateGameSG.link
    )
)

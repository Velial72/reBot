import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ContentType
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import User, CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Column, Start
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput
from aiogram_dialog.widgets.media import StaticMedia
from environs import Env

from tools.LEXICON import LEXICON
from tools.functions import message_send_photo, callback_send_photo

from dialogs.start_module import AdminSG, start_dialog
from dialogs.create_game import create_game_dialog
from dialogs.payment import payment_dialog
from dialogs.my_groups import my_group_dialog
from dialogs.registration import RegistrationSG, registration_dialog

env = Env()
env.read_env()

BOT_TOKEN = env('TELEGRAM_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# работаем без базы
player_data = {
    'player_id': 123,
    'game': True,
    'registration_on_game': True,
    'name': 'Anton',
    'email': 'a@a.ru',
    'wish': 'car'
}

group_data = {
    'admin_id': 12345,
    'game_id': 986532,
    'group_name': '1',
    'description': '',
    'game_date': None,
    'price': '',
    'link': '',

}


@dp.message(CommandStart())
@dp.message(Command(commands=['start']))
async def start_command(message: Message, dialog_manager: DialogManager):
    if ' ' in message.text:
        game_id = int(message.text.split(" ")[-1])
        try:
            game_id == 123
        except:
            await message.answer("Данная игра уже недоступна!")
        #    if Player.objects.filter(
        #             telegram_id=message.from_user.id, game=game).exists():
        #         await message.answer("Вы уже зарегистрированы на эту игру")
        #         return
        #     text_message = LEXICON['game'].format(
        #
        #                      game.name,
        #                      game.start_date,
        #                      game.end_date,
        #                      game.description
        #     )
        #     await message.answer(text=text_message)
        #     await asyncio.sleep(1)
        #     await message.answer(text=LEXICON['user_name'])
        #     await state.set_state(FSMUserForm.user_name)
        await dialog_manager.start(state=RegistrationSG.name, mode=StartMode.RESET_STACK)
    else:
        await message_send_photo(message, 's-bot.jpg')
        await message.answer(text=LEXICON['greeting'])
        await asyncio.sleep(0.2)
        await dialog_manager.start(state=AdminSG.start, mode=StartMode.RESET_STACK)


dp.include_routers(start_dialog,
                   create_game_dialog,
                   payment_dialog,
                   my_group_dialog,
                   registration_dialog
                   )
setup_dialogs(dp)
dp.run_polling(bot)

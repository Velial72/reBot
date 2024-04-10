import importlib
from datetime import date

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import User, CallbackQuery, Message, LabeledPrice
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row, Group, Calendar, Select
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput
from aiogram_dialog.widgets.media import StaticMedia
from environs import Env

from tools.LEXICON import LEXICON

env = Env()
env.read_env()

BOT_TOKEN = env('TELEGRAM_TOKEN')

bot = Bot(token=BOT_TOKEN)


class PaymentSG(StatesGroup):
    start = State()
    finish = State()


async def get_payment(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title='Донат',
        description='Ты творишь добро',
        payload='что-то про payload',
        provider_token=env('YOUKASSA_PAYMENT_TOKEN'),
        currency="RUB",
        start_parameter="test_bot",
        prices=[LabeledPrice(label="руб", amount=10000)]
    )
    await dialog_manager.next()


payment_dialog = Dialog(
    Window(
        Const('Пора сделать подарок создателям бота\n\n'),
        StaticMedia(
            path='media/Scrooge.jpg',
            type=ContentType.PHOTO),
        Button(
            Const('Задонатить 100 руб.'),
            id='on_payment',
            on_click=get_payment
        ),
        state=PaymentSG.start
    ),
    Window(
        Const('Спасибо за поддержку'),
        state=PaymentSG.finish
    )
)


# @dp.message(F.text == LEXICON['payment'], StateFilter(default_state))
# async def get_payment(message: Message, state: FSMContext):
#     # Картинка спасибо за донат
#     text_message = "Пора сделать подарок создателям бота\n\n"
#     kb = [
#         [InlineKeyboardButton(text='Задонатить 100 руб.',
#                               callback_data='payment')]
#     ]
#     await message_send_photo(message, 'Scrooge.jpg')
#     await message.answer(
#         text=text_message,
#         reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
#     )
#     await state.set_state(FSMPaymentForm.payment)

#
# @dp.callback_query(StateFilter(FSMPaymentForm.payment))
# async def get_donat(callback: CallbackQuery, state: FSMContext):
#     await bot.send_invoice(
#         chat_id=callback.from_user.id,
#         title='Донат',
#         description='Ты творишь добро',
#         payload='что-то про payload',
#         provider_token=settings.YOUKASSA_PAYMENT_TOKEN,
#         currency="RUB",
#         start_parameter="test_bot",
#         prices=[LabeledPrice(label="руб", amount=10000)]
#     )
#     await state.set_state(FSMPaymentForm.invoice)
#     await state.clear()
#

# @router.message(StateFilter(FSMPaymentForm.invoice))
# async def send_payment(message: Message, state: FSMContext):
#     print(1)


# @dp.pre_checkout_query()
# async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

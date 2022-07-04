import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode

from db import create_tables
from exceptions import NotCorrectReceipt
from matplot import get_visual_report, get_visual_table_data
from services import add_peceipt, add_new_calc, get_all_calcs, delete_calc, \
    get_dict_of_credits_data, delete_all_calcs, change_calc, get_all_receipts

from texts import *
import environ

env = environ.Env()
environ.Env.read_env()

API_TOKEN = env.get_value('API_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def new_calculation(message: types.Message):
    """Добавление нового расчета"""
    await message.answer(START_TEXT, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['new'])
async def new_calculation(message: types.Message):
    """Добавление нового расчета"""
    alias = message.text[5:]
    add_new_calc(alias, message.from_user.id)
    await message.reply("Новый расчет успешно добавлен")


@dp.message_handler(commands=['all'])
async def all_calculations(message: types.Message):
    """Список всех расчетов"""
    all_calcs = get_all_calcs(message.from_user.id)
    if all_calcs:
        answer = text_all_calcs(all_calcs)
    else:
        answer = 'Отсутствют отчеты с данными'
    await message.reply(answer, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['delall'])
async def del_all_calculations(message: types.Message):
    """Удаление всех расчетов"""
    delete_all_calcs(message.from_user.id)
    answer = f'Все ваши расчеты успешно удалены из базы'
    await message.reply(answer)


@dp.message_handler(commands=['picreport'])
async def pic_reporting(message: types.Message):
    """Получение отчета активного расчета в виде картинки"""
    calc_id, calc_alias, raw_data = get_dict_of_credits_data(message.from_user.id)
    labels, cells = get_visual_table_data(raw_data)
    if cells:
        pic = get_visual_report(labels=labels, cell_text=cells)
        caption = f'Вывод данных об расчете номер {calc_id}, короткое имя - {calc_alias}'
        await message.answer_photo(photo=pic, caption=caption)
    else:
        await message.answer('Данные в расчете отсутствуют')


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_calculation(message: types.Message):
    """Удаление расчета"""
    calc_id = int(message.text[4:])
    delete_result = delete_calc(message.from_user.id, calc_id)
    if delete_result:
        answer = f'Расчет номер {calc_id} успешно удален'
    else:
        answer = f'Расчет под номером {calc_id} в базе отсутствует'
    await message.reply(answer)


@dp.message_handler(commands=['receipts'])
async def all_receipts(message: types.Message):
    """Получение списка всех чеков в текущем расчете"""
    # receipt_id = int(message.text[9:])
    all_receipts = get_all_receipts(message.from_user.id)
    if all_receipts:
        answer = text_all_receipts(all_receipts)
    else:
        answer = f'В текущем расчете чеков не обнаружено'
    await message.reply(answer, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(lambda message: message.text.startswith('/calc'))
async def del_calculation(message: types.Message):
    """Удаление расчета"""
    calc_id = int(message.text[5:])
    _, calc_alias = change_calc(message.from_user.id, calc_id)
    answer = f'Текущий расчет {calc_id} с именем {calc_alias}'
    await message.reply(answer)


@dp.message_handler(lambda message: message.text.startswith('/report'))
async def reporting(message: types.Message):
    """Вывод отчета текущего расчета"""
    persons = str(message.text[8:])
    full_report = False
    sponsor_request, consumer_request = None, None
    if persons:
        sponsor_request, consumer_request = persons.split(' ')
    else:
        full_report = True
    calc_id, calc_alias, report_data = get_dict_of_credits_data(message.from_user.id)
    if report_data:
        answer = text_for_report(calc_id, calc_alias, report_data,
                                         sponsor_request, consumer_request, full_report)
    else:
        answer = 'В вашем текущем расчете отсутствуют данные'
    await message.reply(answer)


@dp.message_handler()
async def add_receipt(message: types.Message):
    """Добавление нового чека"""
    try:
        add_peceipt(message.text, message.from_user.id)
    except NotCorrectReceipt as e:
        answer_message = text(f'Не корректный ввод \n' f'Корректный ввод: \n',
                              italic('Спонсор 1000 Имя1 Имя2  \n'),
                              'Для получения справки введите /help')
        await message.answer(answer_message, reply=False, parse_mode=ParseMode.MARKDOWN)
        return
    answer_message = f'Добавлен чек'
    await message.answer(answer_message, reply=False)


if __name__ == '__main__':
    create_tables()
    executor.start_polling(dp, skip_updates=True)

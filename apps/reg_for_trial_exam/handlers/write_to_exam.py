import datetime
import logging
from config import MESSAGES
from vkbottle.bot import Blueprint, Message
from .. import keyboards
from vk_utils.common_handlers import start_keyboard
from ..state import RegExam
from ..google_api import sheets

SUBJECTS = ['математика',
            'русский',
            'литература',
            'общество',
            'история',
            'английский',
            'биология',
            'химия',
            'математика базовая',
            'математика профильная',
            'без второго',
            'базовая',
            'профильная']
P_SUBJECTS = ['математику',
              'русский',
              'литературу',
              'общество',
              'историю',
              'английский',
              'биологию',
              'химию',
              'математику',
              'математику']
bp = Blueprint()
STORAGE = {}


@bp.on.private_message(text='Записаться на пробный экз.')
async def choice_exam(message: Message):
    now_date = datetime.datetime.now()
    if now_date.weekday() in (4, 5, 6) or \
            (now_date.weekday() == 0 and now_date.hour < 9) or \
            (now_date.weekday() == 3 and now_date.hour >= 17):
        await message.answer(MESSAGES['Запись закончена'],
                             keyboard=None)
        return
    await message.answer('Секунду, я проверю наличие свободных мест.')
    free_places_sut = sheets.get_free_times('СУББОТА')
    free_places_sun = sheets.get_free_times('ВОСКРЕСЕНЬЕ')
    if not any((free_places_sut, free_places_sun)):
        await message.answer(MESSAGES['Отсутствие мест'],
                             keyboard=None)
        return
    logging.info(f'{message.peer_id} начал запись на пробный экзамен')
    STORAGE[message.peer_id] = {}
    STORAGE[message.peer_id]['free_places_sut'] = free_places_sut
    STORAGE[message.peer_id]['free_places_sun'] = free_places_sun
    await message.answer(MESSAGES['Выбор вида экзамена'], keyboard=keyboards.exam_keyboard())
    await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_EXAM)


@bp.on.private_message(state=RegExam.CHOICE_EXAM)
async def choice_first_subject(message: Message):
    if message.text.lower() not in ['егэ', 'огэ']:
        await message.answer(MESSAGES['Несуществующий вид экзамена'], keyboard=keyboards.exam_keyboard())
        return
    STORAGE[message.peer_id]['type_exam'] = message.text.lower()
    await message.answer(MESSAGES['Выбор 1 предмета'], keyboard=keyboards.subjects_keyboard())
    await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_FIRST_SUBJECT)


@bp.on.private_message(state=RegExam.CHOICE_FIRST_SUBJECT)
async def choice_second_subject(message: Message):
    if message.text.lower() not in SUBJECTS:
        await message.answer(MESSAGES['Несуществующий предмет'], keyboard=keyboards.subjects_keyboard())
        return
    elif STORAGE[message.peer_id]['type_exam'] == 'егэ' and message.text.lower() == 'математика':
        await message.answer('Математика базовая или профильная?', keyboard=keyboards.type_math_keyboard())
        return
    if message.text.lower() in ['базовая', 'профильная']:
        STORAGE[message.peer_id]['first_subject'] = f'математика {message.text.lower()}'
    else:
        STORAGE[message.peer_id]['first_subject'] = message.text.lower()
    await message.answer(MESSAGES['Выбор 2 предмета'], keyboard=keyboards.subjects_keyboard(second=True))
    await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_SECOND_SUBJECT)


@bp.on.private_message(state=RegExam.CHOICE_SECOND_SUBJECT)
async def choice_first_day(message: Message):
    if message.text.lower() not in SUBJECTS:
        await message.answer(MESSAGES['Несуществующий предмет'], keyboard=keyboards.subjects_keyboard(second=True))
        return
    elif STORAGE[message.peer_id]['type_exam'] == 'егэ' and message.text.lower() == 'математика':
        await message.answer('Математика базовая или профильная?', keyboard=keyboards.type_math_keyboard())
        return
    if message.text.lower() in ['базовая', 'профильная']:
        STORAGE[message.peer_id]['second_subject'] = f'математика {message.text.lower()}'
    else:
        STORAGE[message.peer_id]['second_subject'] = message.text.lower()
    first_subject = STORAGE[message.peer_id]['first_subject']
    await message.answer(f'{MESSAGES["Выбор дня для 1 предмета"]}'
                         f'{P_SUBJECTS[SUBJECTS.index(first_subject)]}?',
                         keyboard=keyboards.day_keyboard(STORAGE[message.peer_id]['free_places_sut'],
                                                         STORAGE[message.peer_id]['free_places_sun'])
                         )
    await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_FIRST_DAY)


@bp.on.private_message(state=RegExam.CHOICE_FIRST_DAY)
async def choice_second_day(message: Message):
    if message.text.lower() not in ['воскресенье', 'суббота']:
        await message.answer(MESSAGES['Некорректный день'],
                             keyboard=keyboards.day_keyboard(STORAGE[message.peer_id]['free_places_sut'],
                                                             STORAGE[message.peer_id]['free_places_sun'])
                             )
        return
    STORAGE[message.peer_id]['first_day'] = message.text.lower()
    second_subject = STORAGE[message.peer_id]['second_subject']
    if second_subject == 'без второго':
        first_subject = STORAGE[message.peer_id]['first_subject']
        free_places = STORAGE[message.peer_id]['free_places_sut'] if STORAGE[message.peer_id]['first_day'] == 'суббота' \
            else STORAGE[message.peer_id]['free_places_sun']
        STORAGE[message.peer_id]['first_free_places'] = free_places
        await message.answer(
            f'{MESSAGES["Время для 1 предмета"]} {P_SUBJECTS[SUBJECTS.index(first_subject)]}',
            keyboard=keyboards.time_keyboard(free_places))
        await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_FIRST_TIME)
    else:
        await message.answer(f'{MESSAGES["Выбор дня для 2 предмета"]} {P_SUBJECTS[SUBJECTS.index(second_subject)]}?',
                             keyboard=keyboards.day_keyboard(STORAGE[message.peer_id]['free_places_sut'],
                                                             STORAGE[message.peer_id]['free_places_sun'])
                             )
        await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_SECOND_DAY)


@bp.on.private_message(state=RegExam.CHOICE_SECOND_DAY)
async def choice_first_time(message: Message):
    if message.text.lower() not in ['воскресенье', 'суббота']:
        await message.answer(MESSAGES['Некорректный день'],
                             keyboard=keyboards.day_keyboard(STORAGE[message.peer_id]['free_places_sut'],
                                                             STORAGE[message.peer_id]['free_places_sun'])
                             )
        return
    STORAGE[message.peer_id]['second_day'] = message.text.lower()
    first_subject = STORAGE[message.peer_id]['first_subject']
    free_places = STORAGE[message.peer_id]['free_places_sut'] if STORAGE[message.peer_id]['first_day'] == 'суббота' \
        else STORAGE[message.peer_id]['free_places_sun']
    STORAGE[message.peer_id]['first_free_places'] = free_places
    await message.answer(f'{MESSAGES["Время для 1 предмета"]} {P_SUBJECTS[SUBJECTS.index(first_subject)]}',
                         keyboard=keyboards.time_keyboard(free_places))
    await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_FIRST_TIME)


@bp.on.private_message(state=RegExam.CHOICE_FIRST_TIME)
async def choice_second_time(message: Message):
    if message.text.lower() not in STORAGE[message.peer_id]['first_free_places'].keys():
        free_places = STORAGE[message.peer_id]['free_places_sut'] if STORAGE[message.peer_id]['first_day'] == 'суббота' \
            else STORAGE[message.peer_id]['free_places_sun']
        await message.answer(MESSAGES['Некорректное время'],
                             keyboard=keyboards.time_keyboard(free_places))
        return
    STORAGE[message.peer_id]['first_time'] = message.text.lower()
    second_subject = STORAGE[message.peer_id]['second_subject']
    if second_subject == 'без второго':

        users_info = await bp.api.users.get(message.from_id)
        result = sheets.sign_up_to_exam({
            'name': f'{users_info[0].last_name} {users_info[0].first_name}',
            'type_exam': STORAGE[message.peer_id]['type_exam'],
            'first_day': STORAGE[message.peer_id]['first_day'].upper(),
            'first_time': STORAGE[message.peer_id]['first_time'],
            'first_subject': STORAGE[message.peer_id]['first_subject'],
            'first_free_places': STORAGE[message.peer_id]['first_free_places']
        },
            second=False)
        if result:
            await message.answer(
                f"{MESSAGES['Успешная запись']}"
                f"Тип пробного экзамена: {STORAGE[message.peer_id]['type_exam'].upper()}\n"
                f"{STORAGE[message.peer_id]['first_subject']}: {STORAGE[message.peer_id]['first_day']} - {STORAGE[message.peer_id]['first_time']}\n "
            )
            logging.info(f'{message.peer_id} записался')
        else:
            await message.answer(MESSAGES['Ошибка записи'], keyboard=start_keyboard())
            logging.info(f'{message.peer_id} не записался (нехватка места)')
        try:
            del STORAGE[message.peer_id]
        except KeyError:
            logging.warning(f'Не получилось удалить пользователя {message.peer_id}')

        await bp.state_dispenser.delete(message.peer_id)
    else:
        free_places = STORAGE[message.peer_id]['free_places_sut'] if STORAGE[message.peer_id]['second_day'] == 'суббота' \
            else STORAGE[message.peer_id]['free_places_sun']
        STORAGE[message.peer_id]['second_free_places'] = free_places
        await message.answer(f'{MESSAGES["Время для 2 предмета"]} {P_SUBJECTS[SUBJECTS.index(second_subject)]}?',
                             keyboard=keyboards.time_keyboard(free_places))
        await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_SECOND_TIME)


@bp.on.private_message(state=RegExam.CHOICE_SECOND_TIME)
async def finish_reg_exam(message: Message):
    if message.text.lower() not in STORAGE[message.peer_id]['second_free_places'].keys():
        free_places = STORAGE[message.peer_id]['free_places_sut'] if STORAGE[message.peer_id]['second_day'] == 'суббота' \
            else STORAGE[message.peer_id]['free_places_sun']
        await message.answer(MESSAGES['Некорректное время'], keyboard=keyboards.time_keyboard(free_places))
        return
    STORAGE[message.peer_id]['second_time'] = message.text.lower()
    users_info = await bp.api.users.get(message.from_id)
    result = sheets.sign_up_to_exam({
        'name': f'{users_info[0].last_name} {users_info[0].first_name}',
        'type_exam': STORAGE[message.peer_id]['type_exam'],
        'first_day': STORAGE[message.peer_id]['first_day'].upper(),
        'first_time': STORAGE[message.peer_id]['first_time'],
        'first_subject': STORAGE[message.peer_id]['first_subject'],
        'first_free_places': STORAGE[message.peer_id]['first_free_places'],
        'second_day': STORAGE[message.peer_id]['second_day'].upper(),
        'second_time': STORAGE[message.peer_id]['second_time'],
        'second_subject': STORAGE[message.peer_id]['second_subject'],
        'second_free_places': STORAGE[message.peer_id]['second_free_places']
    },
        second=True)
    if result:
        await message.answer(
            f"{MESSAGES['Успешная запись']}"
            f"Тип пробного экзамена: {STORAGE[message.peer_id]['type_exam'].upper()}\n"
            f"{STORAGE[message.peer_id]['first_subject']}: {STORAGE[message.peer_id]['first_day']} - {STORAGE[message.peer_id]['first_time']}\n"
            f"{STORAGE[message.peer_id]['second_subject']}: {STORAGE[message.peer_id]['second_day']} - {STORAGE[message.peer_id]['second_time']}"
        )
        logging.info(f'{message.peer_id} записался')
    else:
        await message.answer(MESSAGES['Ошибка записи'], keyboard=start_keyboard()
        )
        logging.info(f'{message.peer_id} не записался (нехватка места)')
    try:
        del STORAGE[message.peer_id]
    except KeyError:
        logging.warning(f'Не получилось удалить пользователя {message.peer_id}')
    logging.info(f'{message.peer_id} записался')
    await bp.state_dispenser.delete(message.peer_id)

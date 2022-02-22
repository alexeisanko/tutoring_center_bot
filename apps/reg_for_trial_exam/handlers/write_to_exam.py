from vkbottle.bot import Blueprint, Message
from vkbottle import CtxStorage
from .. import keyboards
from utils_vk.common_handlers import start_keyboard
from ..state import RegExam
from ..google_sheets_api import exam

SUBJECTS = ['математика', 'русский', 'литература', 'общество', 'история', 'английский', 'биология', 'без второго']
P_SUBJECTS = ['математику', 'русский', 'литературу', 'общество', 'историю', 'английский', 'биологию']
bp = Blueprint()
STORAGE = CtxStorage()


@bp.on.private_message(text='Записаться на пробный экз.')
async def choice_exam(message: Message):
    await message.answer('Отлично!\n'
                         'К какому экзамену ты готовишься?', keyboard=keyboards.exam_keyboard())
    await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_EXAM)


@bp.on.private_message(state=RegExam.CHOICE_EXAM)
async def choice_first_subject(message: Message):
    if message.text.lower() not in ['егэ', 'огэ']:
        await message.answer('Разве такой экзамен существует? :)\n'
                             'Выберите вид экзамена', keyboard=keyboards.exam_keyboard())
        return
    STORAGE.set('type_exam', message.text.lower())
    await message.answer('Скажи, какие предметы тебя интересуют?', keyboard=keyboards.subjects_keyboard())
    await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_FIRST_SUBJECT)


@bp.on.private_message(state=RegExam.CHOICE_FIRST_SUBJECT)
async def choice_second_subject(message: Message):
    if message.text.lower() not in SUBJECTS:
        await message.answer('Пока мы еще не проводим пробников по такому предмету. Выберите пожалуйста из '
                             'существующих', keyboard=keyboards.subjects_keyboard())
        return
    STORAGE.set('first_subject', message.text.lower())
    await message.answer('Если хотите, вы можете выбрать еще один предмет для пробного экзамена',
                         keyboard=keyboards.subjects_keyboard(second=True))
    await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_SECOND_SUBJECT)


@bp.on.private_message(state=RegExam.CHOICE_SECOND_SUBJECT)
async def choice_first_day(message: Message):
    if message.text.lower() not in SUBJECTS:
        await message.answer('Пока мы еще не проводим пробников по такому предмету. Выберите пожалуйста из '
                             'существующих', keyboard=keyboards.subjects_keyboard(second=True))
        return
    STORAGE.set('second_subject', message.text.lower())
    first_subject = STORAGE.get('first_subject')
    await message.answer(f'Почти готово! Какой день тебе удобнее попробывать написать '
                         f'{P_SUBJECTS[SUBJECTS.index(first_subject)]}  - суббота или воскресенье?',
                         keyboard=keyboards.day_keyboard())
    await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_FIRST_DAY)


@bp.on.private_message(state=RegExam.CHOICE_FIRST_DAY)
async def choice_second_day(message: Message):
    if message.text.lower() not in ['воскресенье', 'суббота']:
        await message.answer('К сожалению мы проводим только в субботу или воскресенье. Попробуйте снова выбрать день',
                             keyboard=keyboards.subjects_keyboard())
        return
    STORAGE.set('first_day', message.text.lower())
    second_subject = STORAGE.get('second_subject')
    if second_subject == 'без второго':
        first_subject = STORAGE.get('first_subject')
        await message.answer(f'Секунду, я проверю наличие свободных мест.')
        await message.answer(
            f'Нашел! Выбери, в какое время ты сможешь прийти на {P_SUBJECTS[SUBJECTS.index(first_subject)]}',
            keyboard=keyboards.time_keyboard(day=message.text.lower()))
        await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_FIRST_TIME)
    else:
        await message.answer(f'А когда будем сдавать {P_SUBJECTS[SUBJECTS.index(second_subject)]}?',
                             keyboard=keyboards.day_keyboard())
        await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_SECOND_DAY)


@bp.on.private_message(state=RegExam.CHOICE_SECOND_DAY)
async def choice_first_time(message: Message):
    if message.text.lower() not in ['воскресенье', 'суббота']:
        await message.answer('К сожалению мы проводим только в субботу или воскресенье. Попробуйте снова выбрать день',
                             keyboard=keyboards.subjects_keyboard())
        return
    STORAGE.set('second_day', message.text.lower())
    first_subject = STORAGE.get('first_subject')
    first_day = STORAGE.get('first_day')
    await message.answer(f'Сейчас проверим есть ли свободное время для записи')
    await message.answer(f'Последний шаг! Выбери, когда ты сможешь прийти на '
                         f'{P_SUBJECTS[SUBJECTS.index(first_subject)]}',
                         keyboard=keyboards.time_keyboard(first_day))
    await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_FIRST_TIME)


@bp.on.private_message(state=RegExam.CHOICE_FIRST_TIME)
async def choice_second_time(message: Message):
    if message.text.lower() not in ['8:00 - 10:00', '10:00 - 12:00', '12:00 - 14:00', '14:00 - 16:00', '16:00 - 18:00']:
        first_day = STORAGE.get('first_day')
        await message.answer('В такое время мы не сможем провести. Выбери пожалуйста из предложенного',
                             keyboard=keyboards.time_keyboard(first_day))
        return
    STORAGE.set('first_time', message.text.lower())
    second_subject = STORAGE.get('second_subject')
    if second_subject == 'без второго':
        await message.answer(
            'Супер! Я записал тебя и буду ждать, когда ты придешь на пробный в эти выходные! Если что-то '
            'пошло не так, пиши в личные сообшения на страницу НьюСкул Пробники'
            '\n\n\n Напомню:\n'
            f"Тип пробного экзамена: {STORAGE.get('type_exam')}\n"
            f"{STORAGE.get('first_subject')}: {STORAGE.get('first_day')} - {STORAGE.get('first_time')}\n",
            keyboard=start_keyboard())
        users_info = await bp.api.users.get(message.from_id)
        exam.sign_up_to_exam({
            'name': users_info[0].first_name,
            'first_day': STORAGE.get('first_day'),
            'first_time': STORAGE.get('first_time'),
            'first_subject': STORAGE.get('first_subject')
        },
            second=False)
        await bp.state_dispenser.delete(message.peer_id)
    else:

        await message.answer(f'А в какое время пойдем на {P_SUBJECTS[SUBJECTS.index(second_subject)]}? ',
                             keyboard=keyboards.time_keyboard(STORAGE.get('second_day')))
        await bp.state_dispenser.set(message.peer_id, RegExam.CHOICE_SECOND_TIME)


@bp.on.private_message(state=RegExam.CHOICE_SECOND_TIME)
async def finish_reg_exam(message: Message):
    if message.text.lower() not in ['8:00 - 10:00', '10:00 - 12:00', '12:00 - 14:00', '14:00 - 16:00', '16:00 - 18:00']:
        await message.answer('В такое время мы не сможем провести. Выбери пожалуйста из предложенного',
                             keyboard=keyboards.time_keyboard(STORAGE.get('second_day')))
        return
    STORAGE.set('second_time', message.text.lower())
    await message.answer('Супер! Я записал тебя и буду ждать, когда ты придешь на пробный в эти выходные! Если что-то '
                         'пошло не так, пиши в личные сообшения на страницу НьюСкул Пробники'
                         '\n\n\n Напомню:\n'
                         f"Тип пробного экзамена: {STORAGE.get('type_exam')}\n"
                         f"{STORAGE.get('first_subject')}: {STORAGE.get('first_day')} - {STORAGE.get('first_time')}\n"
                         f"{STORAGE.get('second_subject')}: {STORAGE.get('second_day')} - {STORAGE.get('second_time')}",
                         keyboard=start_keyboard())
    users_info = await bp.api.users.get(message.from_id)
    exam.sign_up_to_exam({
        'name': users_info[0].first_name,
        'first_day': STORAGE.get('first_day'),
        'first_time': STORAGE.get('first_time'),
        'first_subject': STORAGE.get('first_subject'),
        'second_day': STORAGE.get('second_day'),
        'second_time': STORAGE.get('second_time'),
        'second_subject': STORAGE.get('second_subject')
    },
        second=False)

    await bp.state_dispenser.delete(message.peer_id)

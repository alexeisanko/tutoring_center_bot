from vkbottle import Keyboard, Text, KeyboardButtonColor
from .google_sheets_api import exam


def exam_keyboard():
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text("ОГЭ"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("ЕГЭ"), color=KeyboardButtonColor.POSITIVE)
    return keyboard.get_json()


def subjects_keyboard(second=False):
    keyboard = Keyboard(one_time=True, inline=False)
    subjects = ['Математика', 'Русский', 'Литература', 'Общество', 'История', 'Английский', 'Биология']
    for subject in subjects:
        keyboard.add(Text(subject), color=KeyboardButtonColor.POSITIVE)
        if subject in ('Литература', 'Английский'):
            keyboard.row()
    if second:
        keyboard.add(Text('Без второго'), color=KeyboardButtonColor.POSITIVE)
    return keyboard.get_json()


def day_keyboard():
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text("Суббота"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Воскресенье"), color=KeyboardButtonColor.POSITIVE)
    return keyboard.get_json()


def time_keyboard(day='суббота'):
    times = []
    get_times = exam.get_times_sut if day == 'суббота' else exam.get_time_sun
    for i, j in get_times().items():

        if j[2].count([]) > 0 or len(j[2]) < 8:

            times.append(i)
    keyboard = Keyboard(one_time=True, inline=False)
    for i, time in enumerate(times):
        keyboard.add(Text(time), color=KeyboardButtonColor.POSITIVE)
        if i == 2:
            keyboard.row()
    return keyboard.get_json()



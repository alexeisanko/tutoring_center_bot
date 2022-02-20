from vkbottle import Keyboard, Text, KeyboardButtonColor


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


def time_keyboard():
    times = ['8:00 - 10:00', '10:00 - 12:00', '12:00 - 14:00', '14:00 - 16:00', '16:00 - 18:00']
    keyboard = Keyboard(one_time=True, inline=False)
    for time in times:
        keyboard.add(Text(time), color=KeyboardButtonColor.POSITIVE)
        if time == '10:00 - 12:00':
            keyboard.row()
    return keyboard.get_json()


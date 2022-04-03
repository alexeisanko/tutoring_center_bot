from vkbottle import Keyboard, Text, KeyboardButtonColor


def exam_keyboard():
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text("ОГЭ"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("ЕГЭ"), color=KeyboardButtonColor.POSITIVE)
    return keyboard.get_json()


def subjects_keyboard(second=False):
    keyboard = Keyboard(one_time=True, inline=False)
    if second:
        keyboard.add(Text('Без второго'), color=KeyboardButtonColor.PRIMARY)
    subjects = ['Математика', 'Русский', 'Литература', 'Общество', 'История', 'Английский', 'Биология']
    for subject in subjects:
        if (subjects.index(subject) + 1) / 3 == (subjects.index(subject) + 1) // 3:
            keyboard.row()
        keyboard.add(Text(subject), color=KeyboardButtonColor.POSITIVE)
    return keyboard.get_json()


def day_keyboard(sut, sun):
    keyboard = Keyboard(one_time=True, inline=False)
    if sut:
        keyboard.add(Text("Суббота"), color=KeyboardButtonColor.POSITIVE)
    if sun:
        keyboard.add(Text("Воскресенье"), color=KeyboardButtonColor.POSITIVE)
    return keyboard.get_json()


def time_keyboard(places):
    times = []
    for i, j in places.items():
        times.append(i)
    keyboard = Keyboard(one_time=True, inline=False)
    new_row = True if len(times) > 3 else False
    for i, time in enumerate(times):
        keyboard.add(Text(time), color=KeyboardButtonColor.POSITIVE)
        if i == 2 and new_row:
            keyboard.row()
    return keyboard.get_json()


def type_math_keyboard():
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text("Базовая"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Профильная"), color=KeyboardButtonColor.POSITIVE)
    return keyboard.get_json()
from .get_lessons import get_schedule
from .clock import clock_emoji
import datetime
from json import load


def teachers_n_links():
    with open('teachersnlinks.json', 'r', encoding='utf-8') as file:
        return load(file)


def get_class_string(class_day, schedule):
    teachers_and_links = teachers_n_links()
    teacher_link, full_teacher_name = None, None
    teacher_values = None
    class_name = schedule[class_day]["class"]
    class_link = teachers_and_links.get(class_name)
    class_info = f'<i>{class_name}</i>' if class_name else "<a href=\"https://mrk-bsuir.by/ru/schedule/\">Информация на сайте отсутствует.</a>"
    teacher_name = schedule[class_day]["teacher"]
    if teacher_name:
        teacher_values = teachers_and_links.get(teacher_name)
        if teacher_values:
            teacher_link, full_teacher_name = teacher_values.split('~')
    teacher_info = f'<i><a href="{teacher_link}">{full_teacher_name}</a></i>' if teacher_values else '"Учитель не найден."'
    free_classes = ['Теоретическое обучение', 'Каникулы', 'Преддипломная практика', 'Технологическая практика']

    for name in free_classes:
        if name in class_name:
            return f'\n🔕 Пары нет! {name}.'
    else:
        return (
            f'\n<b>📚 19:20-20:55 | Пара</b>:\n'
            f'<i><a href="{class_link}">"{class_info}"</a></i>'
            f'\n{"👨‍🏫" if teacher_name in ["Воропаев", "Жданович", "Батура"] else "👩‍🏫"}'
            f' <b>Преподаватель</b>:\n<i><a href="{teacher_link}">{teacher_info}</a></i>'
        )


def lessons():
    try:
        now = datetime.datetime.now()
        weekday = now.weekday()

        if weekday in range(0, 5):
            schedule = get_schedule()
            today_class = schedule.get("day active").get("class")

            today_class_string = get_class_string("day active", schedule)
            tomorrow_class_string = get_class_string("day tinted", schedule)

            time_class, time_class_end = (datetime.datetime(year=now.year, month=now.month, day=now.day, hour=19, minute=20),
                                          datetime.datetime(year=now.year, month=now.month, day=now.day, hour=20, minute=55))
            delta = time_class - now
            total_minutes = delta.seconds // 60

            if today_class:
                clock = clock_emoji(now.hour, now.minute)
                if 'Пары нет' in today_class_string:
                    within = f'{clock} <b>Сегодня:\n:</b>\n<i>{today_class}</i>'
                elif time_class <= now <= time_class_end:
                    within = f'{clock} <b>Сегодня:\n❗️19:20 | Идёт пара:</b>\n<i>"{today_class}"</i>'
                elif delta.days < 1 <= total_minutes < 60:
                    within = f'{clock} <b>Сегодня, через {total_minutes} мин. :</b>{today_class_string}'
                elif time_class_end < now:
                    within = f'{clock} <b>Сегодня:\n🥳️ 20:55 | Пара закончилась:</b>\n<i>"{today_class}"</i>'
                else:
                    hours, minutes = divmod(total_minutes, 60)
                    within = f'{clock} <b>Сегодня, через {hours} ч. {minutes} мин. :</b>{today_class_string}'
            else:
                within = '<b>🥺 Я не смог найти информацию о паре на сегодня. </b>'

            tomorrow = tomorrow_class_string
            tomorrow_str = f'\n\n🗓 <b>Завтра:</b><i>{tomorrow_class_string}</i>' if tomorrow else '<b>🥺 Я не смог найти информацию о паре на завтра. </b>'

            return within + tomorrow_str

        elif weekday == 5:
            return '<b>🥳 Сегодня - суббота!</b>'
        elif weekday == 6:
            schedule = get_schedule()
            tomorrow = get_class_string("day tinted", schedule)
            tomorrow_str = f'\n\n🗓 <b>Завтра:</b><i>{get_class_string("day tinted", schedule)}</i>' if tomorrow else '<b>🥺 Я не смог найти информацию о паре на завтра. </b>'
            return (f'<b>🥳 Сегодня - воскресенье!</b>'
                    f'{tomorrow_str}')

    except Exception as e:
        return f"Произошла непредвиденная ошибка: {e}. @dvbsh."

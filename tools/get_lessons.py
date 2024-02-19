from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from datetime import datetime
import requests
import os
import json

BASE_URL = 'https://mrk-bsuir.by'


def fix_name(class_name):
    return class_name.replace('Операцион ные системы', 'Операционные системы')


def get_schedule():
    now = datetime.now()

    info = {
        "last_update": "",
        "day active": {
            "teacher": "",
            "class": ""
        },
        "day tinted": {
            "teacher": "",
            "class": ""
        },
        "followed": ""
    }

    with open('data.json', 'r') as json_data:
        all_json_data = json.load(json_data)
        last_update = datetime.strptime(all_json_data['last_update'], "%Y-%m-%d %H:%M")

    def schedule_parse():
        schedule = BeautifulSoup(requests.get(f"{BASE_URL}/ru/schedule/").text, 'html.parser').find('div',
                                                                                                    class_='schedule')
        for day_class in ['day active', 'day tinted']:
            try:
                schedule_class = schedule.find('a', class_=day_class)
                if schedule_class:
                    response = requests.get(BASE_URL + (schedule_class['href']))

                    with open("temp.pdf", "wb") as pdf:
                        pdf.write(response.content)

                    with open("temp.pdf", "rb") as pdf_file:
                        pdf_reader = PdfReader(pdf_file)
                        text = pdf_reader.pages[6].extract_text()

                    os.remove("temp.pdf")
                    raw_lesson = text[text.find('3К9341'):text.find('2К9341')]
                    if raw_lesson:
                        lesson_info = [i.replace('\n', '') for i in text[text.find('3К9341'):text.find('2К9341')].split(' ')
                                       if i and not any(exclude_item in i for exclude_item in ['3К9341', '3К9342']) and not i == '\n']
                        class_day = int(schedule_class.find_all('div')[0].text)
                        dayclass_info_class = fix_name(' '.join(lesson_info[:-1]))
                        if now.day == class_day and day_class == 'day tinted':

                            if '.' in lesson_info[-1]:
                                info['day active']["teacher"] = lesson_info.pop(-2)
                                info['day active']["class"] = fix_name(' '.join(lesson_info[:-1]))

                            else:
                                info['day active']["teacher"] = lesson_info.pop(-2)
                                info['day active']["class"] = dayclass_info_class

                            info['day tinted']["teacher"] = ''
                            info['day tinted']["class"] = ''
                            break

                        if '.' in lesson_info[-1]:
                            info[day_class]["teacher"] = lesson_info.pop(-2)
                            info[day_class]["class"] = fix_name(' '.join(lesson_info[:-1]))
                        else:
                            info[day_class]["teacher"] = lesson_info.pop(-1)
                            info[day_class]["class"] = dayclass_info_class

            except Exception as err:
                print(err)

            info["last_update"] = now.strftime("%Y-%m-%d %H:%M")
            info["followed"] = all_json_data["followed"]

            with open('data.json', 'w', encoding='utf-8') as file:
                file.write(json.dumps(info, indent=4))

            return info

    if now.day != last_update.day or last_update.hour < 16 or (now.hour - last_update.hour >= 2):
        print(f'Последний раз данные обновлялись {last_update}.')
        schedule_info = schedule_parse()
    else:
        try:
            with open('data.json', 'r') as json_data:
                all_data = json.load(json_data)
                schedule_info = all_data
                print(f'Данные были успешно загружены из data.json!')
        except [KeyError, FileNotFoundError] as e:
            print(f'Ошибка {e}. Получаем новые данные.')
            schedule_info = schedule_parse()

    return schedule_info

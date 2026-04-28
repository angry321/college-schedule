import os
import sys
import pandas as pd
import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import PATH_TO_TABLE

OFFICE = 31
GROUP_COL = 30
TIME_COL = 3
DAY_COL = 1
NUMBER_COL = 2

if PATH_TO_TABLE and os.path.exists(PATH_TO_TABLE):
    df = pd.read_excel(PATH_TO_TABLE, header=None)
else:
    df = None

days = {
    0: "ПОНЕДЕЛЬНИК",
    1: "ВТОРНИК",
    2: "СРЕДА",
    3: "ЧЕТВЕРГ",
    4: "ПЯТНИЦА",
    5: "СУББОТА"
}


def get_today_schedule():
    # если файла нет или он не найден
    if df is None or df.empty:
        return "Файл с расписанием пустой или не найден"

    weekday_num = datetime.datetime.now().weekday()
    today_name = days.get(weekday_num)
    
    if today_name is None:
        return "Сегодня пар нет"

    schedule = []
    collect = False

    for i in range(len(df)):
        row = df.iloc[i]

        cell_raw = row[DAY_COL]

        if pd.isna(cell_raw):
            cell = ""
        else:
            cell = str(cell_raw)

        if today_name in cell:
            collect = True
        elif collect and cell != "":
            break

        if collect:
            time = row[TIME_COL]
            lesson = row[GROUP_COL]
            office = row[OFFICE]
            number = row[NUMBER_COL]
            
            # замена nan
            if pd.isna(office):
                office = "-"
            else:
                office = str(office)
            
            if pd.isna(number):
                number = "-"
            else:
                number = str(number)

            if pd.notna(time) and pd.notna(lesson):
                lesson = str(lesson)

                if "уб." not in lesson.lower():
                    schedule.append(f"{number}) {time} — {lesson}. КАБИНЕТ: {office}")

    if schedule:
        return f"{today_name}:\n" + "\n".join(schedule)
    else:
        return "Сегодня пар нет"


if __name__ == "__main__":
    print(get_today_schedule())

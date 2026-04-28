import os
import sys
import pandas as pd

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

WEEK_DAYS = ["ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА", "ЧЕТВЕРГ", "ПЯТНИЦА", "СУББОТА"]


def get_week_schedule():
    # если файла нет или он пустой
    if df is None or df.empty:
        return {}

    schedule = {}
    current_day = None

    for i in range(len(df)):
        row = df.iloc[i]

        # нашли день недели
        if isinstance(row[DAY_COL], str):
        	day_text = row[DAY_COL].strip()
        	if any(day in day_text for day in WEEK_DAYS):
        		current_day = day_text
        		if current_day not in schedule:
        			schedule[current_day] = []

        if current_day:
            time = row[TIME_COL]
            lesson = row[GROUP_COL]
            office = row[OFFICE]
            number = row[NUMBER_COL]
            
            # Обработка номера пары
            if pd.isna(number):
                number = "-"
            else:
                number = str(number)
            
            # Обработка кабинета
            if pd.isna(office):
                office = "-"
            else:
                office = str(office)

            if pd.notna(time) and pd.notna(lesson):
                lesson = str(lesson)

                if "уб." not in lesson.lower():
                    schedule[current_day].append(
                        f"{number}) {time} — {lesson}. КАБИНЕТ: {office}"
                    )

    return schedule


def format_week_schedule(schedule: dict):
    result = ""

    for day, lessons in schedule.items():
        if lessons:
            result += f"{day}\n"
            result += "\n".join(lessons)
            result += "\n\n"

    return result.strip() if result else "Файл с расписанием пустой или не найден"


if __name__ == "__main__":
    schedule = get_week_schedule()
    print(format_week_schedule(schedule))

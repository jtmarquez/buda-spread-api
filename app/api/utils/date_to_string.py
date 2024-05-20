from datetime import datetime


def string_to_date(date: datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M:%S")

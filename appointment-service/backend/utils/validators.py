from datetime import date, time, datetime
from typing import Union

def validate_future_date(date_str: Union[str, date]) -> bool:
    """Validate that a date is in the future"""
    if isinstance(date_str, str):
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return False
    else:
        date_obj = date_str

    return date_obj >= date.today()

def validate_time_format(time_str: Union[str, time]) -> bool:
    """Validate time format"""
    try:
        if isinstance(time_str, str):
            datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

from datetime import datetime


def generate_iso_date(date_str: str = None) -> str:
    if date_str:
        return datetime.strptime(date_str, '%Y-%m-%d').isoformat()
    return datetime.now().strftime('%Y-%m-%d')

def generate_iso_datetime(datetime_str: str = None) -> str:
    format_string = '%Y-%m-%d-%H%M%S'
    if datetime_str:
        return datetime.strptime(datetime_str, format_string).isoformat()
    return datetime.now().strftime(format_string)


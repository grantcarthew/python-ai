from datetime import datetime


def generate_iso_date(date_str: str = None) -> str:
    if date_str:
        return datetime.strptime(date_str, '%Y-%m-%d').isoformat()
    return datetime.now().strftime('%Y-%m-%d')

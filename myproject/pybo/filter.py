import locale
locale.setlocale(locale.LC_ALL, '')

def format_datetime(value, fmt='%Y년 %m월 %d일 %H:%M'): #날짜 필터링
    return value.strftime(fmt)
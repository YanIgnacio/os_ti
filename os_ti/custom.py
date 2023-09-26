
from datetime import datetime
import calendar

def month_translate(value):
    month, year = value.split()
    months_dict = {
        'Jan': 'Janeiro',
        'Feb': 'Fevereiro',
        'Mar': 'Março',
        'Apr': 'Abril',
        'May': 'Maio',
        'Jun': 'junho',
        'Jul': 'julho',
        'Aug': 'agosto',
        'Sep': 'setembro',
        'Oct': 'outubro',
        'Nov': 'novembro',
        'Dec': 'dezembro',
    }
    translated_month = months_dict.get(month, month)
    return f"{translated_month} {year}"
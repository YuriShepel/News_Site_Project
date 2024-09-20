from datetime import timedelta
from django.utils import timezone
from django.utils.text import slugify
import re


def declension(number, words):
    cases = [2, 0, 1, 1, 1, 2]
    if 4 < number % 100 < 20:
        return words[2]
    else:
        return words[cases[min(number % 10, 5)]]


def time_since_published(published_date):
    # Показывает время с момента публикации поста
    now = timezone.now()
    diff = now - published_date

    if diff < timedelta(minutes=1):
        return 'только что'
    elif diff < timedelta(hours=1):
        minutes = diff.seconds // 60
        return f'{minutes} {declension(minutes, ["минуту", "минуты", "минут"])} назад'
    elif diff < timedelta(days=1):
        hours = diff.seconds // 3600
        return f'{hours} {declension(hours, ["час", "часа", "часов"])} назад'
    elif diff < timedelta(days=30):
        days = diff.days
        return f'{days} {declension(days, ["день", "дня", "дней"])} назад'
    elif diff < timedelta(days=365):
        months = diff.days // 30
        return f'{months} {declension(months, ["месяц", "месяца", "месяцев"])} назад'
    else:
        years = diff.days // 365
        return f'{years} {declension(years, ["год", "года", "лет"])} назад'


def get_short_body(body, length=500):
    # Отображает определенное количество символов поста
    if len(body) <= length:
        return body
    return body[:length] + '...'


def custom_slugify(value):
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return slugify(value, allow_unicode=True)
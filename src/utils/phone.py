# src/utils/phone.py

import re


def normalize_phone(raw: str, country_code: str = "+7") -> str | None:
    """
    Примитивная нормализация телефона в формат типа +7XXXXXXXXXX.
    Если телефон не удаётся привести, вернуть None.
    """
    if not raw:
        return None

    digits = re.sub(r"\D", "", raw)

    # Пример для Казахстана/РФ: 11 цифр, начинается с 7 или 8
    if len(digits) == 11 and digits[0] in ("7", "8"):
        return "+7" + digits[1:]

    # Если 10 цифр – считаем, что локальный без кода
    if len(digits) == 10:
        return country_code + digits

    return None

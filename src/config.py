import os
from dotenv import load_dotenv

load_dotenv()

AMOCRM_BASE_URL = os.getenv("AMOCRM_BASE_URL")
AMOCRM_ACCESS_TOKEN = os.getenv("AMOCRM_ACCESS_TOKEN")
AMOCRM_REFRESH_TOKEN = os.getenv("AMOCRM_REFRESH_TOKEN")
AMOCRM_CLIENT_ID = os.getenv("AMOCRM_CLIENT_ID")
AMOCRM_CLIENT_SECRET = os.getenv("AMOCRM_CLIENT_SECRET")

MACDENT_API_URL = os.getenv("MACDENT_API_URL")
MACDENT_API_TOKEN = os.getenv("MACDENT_API_TOKEN")

META_ADS_ACCESS_TOKEN = os.getenv("META_ADS_ACCESS_TOKEN")
META_ADS_ACCOUNT_ID = os.getenv("META_ADS_ACCOUNT_ID")

DB_URL = os.getenv("DB_URL")

AMO_STATUS_MAP = {
    1: "Новый лид",
    2: "НДЗ / ИГНОР",
    3: "Перезвонить позже",
    4: "Отвеченные",
    5: "Условный отказ",
    6: "Холодные лиды",
    7: "Квалифицирован",
    8: "Договариваемся о времени",
    9: "Записан",
    10: "Отменил запись",
    11: "Пришел / был на встрече",
    12: "Не пришел",
    13: "Принимает решение",
    14: "Вторичная оплата",
}

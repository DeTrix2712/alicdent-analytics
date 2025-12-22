import os
from dotenv import load_dotenv

load_dotenv()

AMOCRM_BASE_URL = os.getenv("AMOCRM_BASE_URL")
AMOCRM_TOKEN = os.getenv("AMOCRM_TOKEN")
AMOCRM_PIPELINE_ID = int(os.getenv("AMOCRM_PIPELINE_ID") or 0)

MACDENT_API_URL = os.getenv("MACDENT_API_URL")
MACDENT_API_TOKEN = os.getenv("MACDENT_API_TOKEN")

META_ADS_ACCESS_TOKEN = os.getenv("META_ADS_ACCESS_TOKEN")
META_ADS_ACCOUNT_ID = os.getenv("META_ADS_ACCOUNT_ID")

DB_URL = os.getenv("DB_URL")

AMO_STATUS_MAP = None

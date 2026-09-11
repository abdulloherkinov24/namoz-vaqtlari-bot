from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
API_URL = os.getenv('API_URL', 'https://islomapi.uz/api/prayer')

# Regions mapping (IDs used when calling the API)
REGIONS = {
    '1': 'Toshkent shahri',
    '2': 'Toshkent viloyati',
    '3': 'Samarqand',
    '4': 'Buxoro',
    '5': 'Xorazm',
    '6': 'Navoi',
    '7': "Qashqadarya",
    '8': 'Surxondarya',
    '9': 'Andijon',
    '10': "Farg'ona",
    '11': 'Namangan',
    '12': 'Jizzax',
    '13': "Qoraqalpog'iston Respublikasi",
}


def get_region_name(region_id):
    """Return human-friendly region name for a given id."""
    return REGIONS.get(str(region_id), "Noma'lum")


def validate_env():
    """Check required environment variables and return list of missing ones."""
    missing = []
    if not TELEGRAM_TOKEN:
        missing.append('TELEGRAM_TOKEN')
    if not API_URL:
        missing.append('API_URL')
    return missing


__all__ = [
    'TELEGRAM_TOKEN',
    'API_URL',
    'REGIONS',
    'get_region_name',
    'validate_env',
]

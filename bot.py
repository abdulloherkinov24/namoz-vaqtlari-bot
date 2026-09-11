import telebot
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
API_URL = os.getenv('API_URL', 'https://islomapi.uz/api/prayer')

# Initialize bot
bot = telebot.TeleBot(TOKEN)

# Store user location
user_locations = {}

# Prayer times data - 13 viloyat + Qoraqalpog'iston
REGIONS = {
    '1': 'Toshkent shahri',
    '2': 'Toshkent viloyati',
    '3': 'Samarqand',
    '4': 'Buxoro',
    '5': 'Xorazm',
    '6': 'Navoi',
    '7': 'Qashqadarya',
    '8': 'Surxondarya',
    '9': 'Andijon',
    '10': "Farg'ona",
    '11': 'Namangan',
    '12': 'Jizzax',
    '13': "Qoraqalpog'iston Respublikasi",
}


def first_existing(d: dict, keys):
    """Return the first existing key from keys list in dict d, or 'N/A'."""
    for k in keys:
        if k in d and d[k]:
            return d[k]
    return 'N/A'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Start command - show main menu with a "Namoz vaqtlari" button."""
    text = (
        "👋 Assalomu alaykum!\n\n"
        "Men Namoz Vaqtlari Boti-man. Siz viloyat bo'yicha namoz vaqtlarini ko'rishingiz mumkin.\n\n"
        "Quyidagi tugmalardan birini tanlang:\n"
    )

    markup = telebot.types.InlineKeyboardMarkup()
    # Main menu button
    markup.add(telebot.types.InlineKeyboardButton("🕌 Namoz vaqtlari", callback_data="open_prayer"))
    # Optional extra buttons can be added later

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'open_prayer')
def open_prayer_menu(call):
    """Show regions when the user presses the Namoz vaqtlari button."""
    markup = telebot.types.InlineKeyboardMarkup()
    buttons = []
    for key, region in REGIONS.items():
        buttons.append(telebot.types.InlineKeyboardButton(region, callback_data=f"region_{key}"))

    # Add buttons two per row
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.row(buttons[i], buttons[i + 1])
        else:
            markup.add(buttons[i])

    bot.edit_message_text("📍 Viloyatni tanlang:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('region_'))
def select_region(call):
    """Handle region selection: save user region and immediately show prayer times."""
    region_id = call.data.split('_', 1)[1]
    region_name = REGIONS.get(region_id, "Noma'lum")

    user_locations[call.from_user.id] = {
        'region_id': region_id,
        'region_name': region_name
    }

    bot.answer_callback_query(call.id, text=f"{region_name} tanlandi — namoz vaqtlarini olish...")

    # Fetch and send times immediately
    send_prayer_times(call.message.chat.id, region_id, region_name)


def send_prayer_times(chat_id, region_id, region_name):
    """Fetch prayer times from API and send formatted message to chat_id with debug info."""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        url = f"{API_URL}?region={region_id}&date={today}"
        print("DEBUG: Requesting URL:", url)  # konsol log
        response = requests.get(url, timeout=10)

        print("DEBUG: status_code:", response.status_code)
        # log first 800 chars of body to avoid huge logs
        body_preview = response.text[:800].replace('\n', ' ')
        print("DEBUG: body preview:", body_preview)

        if response.status_code != 200:
            bot.send_message(chat_id, f"❌ API-dan ma'lumot olib bo'lmadi. Status: {response.status_code}\n\n{body_preview}")
            return

        data = response.json()
        # Try to find 'times' in different possible shapes
        times = {}
        if isinstance(data, dict):
            # Common structures: {'data': {'times': {...}}} or {'times': {...}} or {'result': {...}}
            if 'data' in data and isinstance(data['data'], dict) and 'times' in data['data']:
                times = data['data']['times']
            elif 'times' in data:
                times = data['times']
            elif 'result' in data and isinstance(data['result'], dict) and 'times' in data['result']:
                times = data['result']['times']
            else:
                # As a fallback, try to find first nested dict that contains likely prayer keys
                for v in data.values():
                    if isinstance(v, dict):
                        keys = set(v.keys())
                        if keys & set(['fajr','sunrise','dhuhr','asr','maghrib','isha','tangle','quyosh','peshin','shom','xufton']):
                            times = v
                            break

        # if still empty, inform and show helpful hint
        if not times:
            bot.send_message(chat_id, "⚠️ API javobidan namoz vaqtlarini topolmadim. Iltimos keyinroq urinib ko'ring.\n\n(Administrator: tekshirish uchun raw API preview loglarni qarang.)")
            return

        # Robust key lookup for each prayer
        bomdod = first_existing(times, ['tangle', 'bomdod', 'fajr'])
        quyosh = first_existing(times, ['quyosh', 'sunrise'])
        peshin = first_existing(times, ['peshin', 'dhuhr'])
        asr = first_existing(times, ['asr'])
        shom = first_existing(times, ['shom', 'maghrib'])
        xufton = first_existing(times, ['xufton', 'isha'])

        text = f"🕌 {region_name} - Namoz Vaqtlari\n"
        text += f"📅 {today}\n\n"
        text += f"🌅 Bomdod: {bomdod}\n"
        text += f"☀️ Quyosh: {quyosh}\n"
        text += f"🌤️ Peshin: {peshin}\n"
        text += f"🌆 Asr: {asr}\n"
        text += f"🌇 Shom: {shom}\n"
        text += f"🌙 Xufton: {xufton}\n"

        bot.send_message(chat_id, text)

    except Exception as e:
        print(f"Error fetching prayer times: {e}")
        bot.send_message(chat_id, f"❌ Xatolik: {str(e)}")


@bot.message_handler(commands=['prayer'])
def get_prayer_times(message):
    """Backward-compatible /prayer command: if user already selected a region, show times, otherwise ask to choose."""
    user_id = message.from_user.id

    if user_id not in user_locations:
        text = "⚠️ Avval viloyatni tanlang! /start yoki 🕌 Namoz vaqtlari tugmasini bosing."
        bot.send_message(message.chat.id, text)
        return

    region_id = user_locations[user_id]['region_id']
    region_name = user_locations[user_id]['region_name']
    send_prayer_times(message.chat.id, region_id, region_name)


@bot.message_handler(commands=['regions'])
def show_regions(message):
    """Show all available regions as a text list."""
    text = "📍 *Mavjud Viloyatlar:*\n\n"
    for key, region in REGIONS.items():
        text += f"{key}. {region}\n"

    text += "\n/start - Viloyat tanlash uchun"
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=['help'])
def send_help(message):
    """Show help message"""
    text = (
        "📖 Buyruqlar:\n\n"
        "/start - Asosiy menyu\n"
        "/prayer - Namoz vaqtlarini ko'rish (agar viloyat tanlangan bo'lsa)\n"
        "/regions - Barcha viloyatlarni ko'rish\n"
        "/help - Yordam\n\n"
        "ℹ️ Ma'lumot: Bot O'zbekistonning 13 viloyati va Qoraqalpog'iston uchun namoz vaqtlarini ko'rsatadi.\n"
        "👨‍💻 Bot dev: @abdulloherkinov24"
    )
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['change'])
def change_region(message):
    """Change region without /start (open the regions menu)."""
    send_welcome(message)


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    """Handle any other message"""
    text = "Kechirasiz, bu buyruqni tushunmadim.\n\n/help - Yordam uchun\n/start - Viloyat tanlash uchun"
    bot.send_message(message.chat.id, text)


# Start polling
if __name__ == '__main__':
    print("🤖 Namoz Vaqtlari Boti ishga tushdi...")
    print(f"📍 Viloyatlar soni: {len(REGIONS)}")
    bot.infinity_polling()

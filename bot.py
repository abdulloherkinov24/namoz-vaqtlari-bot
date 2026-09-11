import telebot
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
API_URL = os.getenv('API_URL')

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
    '10': 'Farg\'ona',
    '11': 'Namangan',
    '12': 'Jizzax',
    '13': 'Qoraqalpog\'iston Respublikasi',
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Start command - show welcome message"""
    text = """
👋 Assalomu alaikum! 🕌

Men Namoz Vaqtlari Boti-man. 
Uzbekiston-ning 13 viloyati va Qoraqalpog'iston uchun 
namoz vaqtlarini ko'rsataman.

Viloyatingizni tanlang:
"""
    markup = telebot.types.InlineKeyboardMarkup()
    
    # Create buttons in 2 columns for better UI
    buttons = []
    for key, region in REGIONS.items():
        buttons.append(telebot.types.InlineKeyboardButton(
            region, 
            callback_data=f"region_{key}"
        ))
    
    # Add buttons 2 per row
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.row(buttons[i], buttons[i + 1])
        else:
            markup.add(buttons[i])
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('region_'))
def select_region(call):
    """Handle region selection"""
    region_id = call.data.split('_')[1]
    region_name = REGIONS.get(region_id, 'Noma\'lum')
    
    user_locations[call.from_user.id] = {
        'region_id': region_id,
        'region_name': region_name
    }
    
    text = f"✅ {region_name} tanlandi!\n\nNamoz vaqtlarini ko'rish uchun /prayer yozing"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

@bot.message_handler(commands=['prayer'])
def get_prayer_times(message):
    """Get prayer times for selected region"""
    user_id = message.from_user.id
    
    if user_id not in user_locations:
        text = "⚠️ Avval viloyatni tanlang! /start buyrug'ini ishlating."
        bot.send_message(message.chat.id, text)
        return
    
    region_id = user_locations[user_id]['region_id']
    region_name = user_locations[user_id]['region_name']
    
    try:
        # Get current date
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Fetch prayer times from API
        response = requests.get(f"{API_URL}?region={region_id}&date={today}")
        
        if response.status_code == 200:
            data = response.json()
            times = data.get('data', {}).get('times', {})
            
            text = f"🕌 *{region_name} - Namoz Vaqtlari*\n"
            text += f"📅 {today}\n\n"
            text += f"🌅 Bomdod: {times.get('tangle', 'N/A')}\n"
            text += f"☀️ Quyosh: {times.get('quyosh', 'N/A')}\n"
            text += f"🌤️ Peshin: {times.get('peshin', 'N/A')}\n"
            text += f"🌆 Asr: {times.get('asr', 'N/A')}\n"
            text += f"🌇 Shom: {times.get('shom', 'N/A')}\n"
            text += f"🌙 Xufton: {times.get('xufton', 'N/A')}\n"
            
            bot.send_message(message.chat.id, text, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "❌ API-dan ma'lumot olib bo'lmadi. Keyinroq qayta urining.")
    
    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, f"❌ Xatolik: {str(e)}")

@bot.message_handler(commands=['regions'])
def show_regions(message):
    """Show all available regions"""
    text = "📍 *Mavjud Viloyatlar:*\n\n"
    for key, region in REGIONS.items():
        text += f"{key}. {region}\n"
    
    text += "\n/start - Viloyat tanlash uchun"
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def send_help(message):
    """Show help message"""
    text = """
📖 *Buyruqlar:*

/start - Viloyat tanlash
/prayer - Namoz vaqtlarini ko'rish
/regions - Barcha viloyatlarni ko'rish
/help - Yordam

ℹ️ *Ma'lumot:*
Bot Uzbekiston-ning barcha 13 viloyati va 
Qoraqalpog'iston Respublikasi uchun namoz vaqtlarini ko'rsatadi.

👨‍💻 Bot dev: @abdulloherkinov24
"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['change'])
def change_region(message):
    """Change region without /start"""
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

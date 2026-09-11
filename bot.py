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

# Prayer times data
REGIONS = {
    '1': 'Toshkent',
    '2': 'Samarqand',
    '3': 'Buxoro',
    '4': 'Xiva',
    '5': 'Andijon',
    '6': 'Farg\'ona',
    '7': 'Qo\'qon',
    '8': 'Nurafshon',
    '9': 'Qashqadarya',
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Start command - show welcome message"""
    text = """
👋 Assalomu alaikum! 🕌

Men Namoz Vaqtlari Boti-man. 
Sizning shaharingiz uchun namoz vaqtlarini ko'rsataman.

Shaharni tanlang:
"""
    markup = telebot.types.InlineKeyboardMarkup()
    
    for key, city in REGIONS.items():
        markup.add(telebot.types.InlineKeyboardButton(
            city, 
            callback_data=f"city_{key}"
        ))
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('city_'))
def select_city(call):
    """Handle city selection"""
    city_id = call.data.split('_')[1]
    city_name = REGIONS.get(city_id, 'Noma\'lum')
    
    user_locations[call.from_user.id] = {
        'city_id': city_id,
        'city_name': city_name
    }
    
    text = f"✅ {city_name} tanlandi!\n\nNamoz vaqtlarini ko'rish uchun /prayer yozing"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

@bot.message_handler(commands=['prayer'])
def get_prayer_times(message):
    """Get prayer times for selected city"""
    user_id = message.from_user.id
    
    if user_id not in user_locations:
        text = "⚠️ Avval shaharni tanlang! /start buyrug'ini ishlating."
        bot.send_message(message.chat.id, text)
        return
    
    city_id = user_locations[user_id]['city_id']
    city_name = user_locations[user_id]['city_name']
    
    try:
        # Get current date
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Fetch prayer times from API
        response = requests.get(f"{API_URL}?region={city_id}&date={today}")
        
        if response.status_code == 200:
            data = response.json()
            times = data.get('data', {}).get('times', {})
            
            text = f"🕌 *{city_name} - Namoz Vaqtlari*\n"
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

@bot.message_handler(commands=['help'])
def send_help(message):
    """Show help message"""
    text = """
📖 *Buyruqlar:*

/start - Shahar tanlash
/prayer - Namoz vaqtlarini ko'rish
/help - Yordam

👨‍💻 Bot dev: @abdulloherkinov24
"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    """Handle any other message"""
    text = "Kechirasiz, bu buyruqni tushunmadim. /help yozing."
    bot.send_message(message.chat.id, text)

# Start polling
if __name__ == '__main__':
    print("🤖 Bot ishga tushdi...")
    bot.infinity_polling()

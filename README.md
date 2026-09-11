# 🕌 Namoz Vaqtlari Telegram Boti

Uzbekiston-ning barcha **13 viloyati** va **Qoraqalpog'iston Respublikasi** uchun namoz vaqtlarini ko'rsatuvchi Telegram bot.

## ✨ Xususiyatlari

- 📍 **13 Viloyat + Qoraqalpog'iston** (Jami 14 ta zona)
- 🕐 **Har kunlik namoz vaqtlari** (6 vaqt)
- 🌍 **Islomapi API integratsiyasi**
- 🤖 **Oson va sodda interfeys**
- 💾 **User memory** (Viloyat saqlanib turadi)
- 🎨 **Responsive button layout**

## 📍 Qo'llash Viloyatlari

1. Toshkent shahri
2. Toshkent viloyati
3. Samarqand
4. Buxoro
5. Xorazm
6. Navoi
7. Qashqadarya
8. Surxondarya
9. Andijon
10. Farg'ona
11. Namangan
12. Jizzax
13. Qoraqalpog'iston Respublikasi

## 🚀 O'rnatish va Ishga Tushirish

### 1️⃣ Repository-ni Clone Qiling

```bash
git clone https://github.com/abdulloherkinov24/namoz-vaqtlari-bot.git
cd namoz-vaqtlari-bot
```

### 2️⃣ Virtual Environment Yarating

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Dependencies O'rnatish

```bash
pip install -r requirements.txt
```

### 4️⃣ .env Fayli Yarating

```bash
# Terminal-da
echo "TELEGRAM_TOKEN=YOUR_BOT_TOKEN_HERE" > .env
echo "API_URL=https://islomapi.uz/api/prayer" >> .env
```

Yoki `.env` faylini text editor-da oching va quyidagini yozing:

```
TELEGRAM_TOKEN=8999548529:AAHCtz0erXFzPJoZnJTBYm2G0NRDTzsY0h8
API_URL=https://islomapi.uz/api/prayer
```

**⚠️ Eslatma:** `TELEGRAM_TOKEN` o'rniga o'z tokeningizni qo'ying!

### 5️⃣ Botni Ishga Tushiring

```bash
python bot.py
```

Agar hammasi to'g'ri bo'lsa, quyidagini ko'rasiz:
```
🤖 Namoz Vaqtlari Boti ishga tushdi...
📍 Viloyatlar soni: 14
```

## 📝 Bot Buyruqlari

| Buyruq | Tavsif |
|--------|--------|
| `/start` | Viloyat tanlash sahifasini ko'rish |
| `/prayer` | Tanlangan viloyat uchun namoz vaqtlarini ko'rish |
| `/regions` | Barcha viloyatlarning ro'yxatini ko'rish |
| `/change` | Viloyatni o'zgartirish |
| `/help` | Yordam va ma'lumot |

## 🕐 Namoz Vaqtlari

Bot quyidagi 6 ta namoz vaqtini ko'rsatadi:

- 🌅 **Bomdod** (Fajr) - Tong saharida
- ☀️ **Quyosh** (Sunrise) - Quyosh ko'tarilishi
- 🌤️ **Peshin** (Dhuhr) - Kunning o'rtasi
- 🌆 **Asr** (Asr) - Kunning soat ikkinchi yarmi
- 🌇 **Shom** (Maghrib) - Quyosh botgandan keyin
- 🌙 **Xufton** (Isha) - Kechqurun

## 🔧 Texnologiyalar

```
Python 3.8+
pyTelegramBotAPI==4.14.0  - Telegram bot API
requests==2.31.0          - HTTP so'rovlar
python-dotenv==1.0.0      - Environment variables
```

## 📚 API Manbalar

- **Islomapi** - https://islomapi.uz/
  - Uzbekiston uchun namoz vaqtlari
  - Bepul va ochiq API

## 📁 Fayl Strukturasi

```
namoz-vaqtlari-bot/
├── bot.py                 # 🤖 Asosiy bot kodi
├── requirements.txt       # 📦 Python dependencies
├── .env                   # 🔐 Token va API URL (xavfsiz)
├── .gitignore            # 🚫 Git-ga shu'tkilmaydigan fayllar
├── README.md             # 📖 Bu fayl
└── .github/
    └── workflows/        # GitHub Actions (future)
```

## 🔐 Xavfsizlik

### ⚠️ DIQQAT!

`.env` faylidagi `TELEGRAM_TOKEN` juda muhim! 

**Hech kimga bermang!** Kimdir tokenni olib qolsa:
- Bot-ni hech kimga yuborib qo'yolmaysiz
- Bot-da kalte kirmaydilari

**Agar token leak bo'lsa:**
1. Darhol @BotFather ga yozing
2. `/mybots` → botingizni tanlang
3. `Revoke current token` bosing
4. Yangi token oling
5. `.env` faylni yangilang
6. Botni qayta ishga tushiring

## 🐛 Xatolikni Tuzatish

### Bot javob bermayapti?

```bash
# 1. Token to'g'ri yozilganini tekshiring
cat .env

# 2. Internet bor-yo'qligini tekshiring
ping islomapi.uz

# 3. Python versiyasini tekshiring
python --version  # 3.8+ bo'lishi kerak

# 4. Dependencies o'rnatilganini tekshiring
pip list | grep -E "telebot|requests|python-dotenv"
```

### API xatoliklar?

Agar API xatolik bersa:
- API server vaqt-vaqt ishlamay qolishi mumkin
- Internet ulanishi tekshiring
- Viloyat ID-si to'g'ri bo'lishini tekshiring

## 🚀 Keyingi Features

- [ ] Database qo'shish (user preferences saqlanadi)
- [ ] Bugungi namoz vaqtini xabarnoma qilish
- [ ] Hijri kalendarini ko'rish
- [ ] Namoz surasini o'qish
- [ ] Multi-language support

## 👨‍💻 Muallif

**[@abdulloherkinov24](https://github.com/abdulloherkinov24)**

## 📄 Litsenziya

MIT License - Bepul va ochiq kodli

---

## 💬 Aloqa

Savollar yoki masalalar bo'lsa:
- GitHub Issues: https://github.com/abdulloherkinov24/namoz-vaqtlari-bot/issues
- Telegram: @abdulloherkinov24

## 🙏 Du'o

Ushbu bot Islom din-ga xizmat qilish va ummatga foyda berish maqsadida yaratildi.

**Barkalik! 🕌**

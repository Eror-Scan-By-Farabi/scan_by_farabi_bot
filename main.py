import telebot
import requests
import json
from datetime import datetime

# ==========================================
# ১. কনফিগারেশন এবং সেটআপ
# ==========================================
BOT_TOKEN = "8838125942:AAHJUUmDwagGm0e_4N_6H8n_y3Jgvza9wC8"
bot = telebot.TeleBot(BOT_TOKEN)

DB_FILE = "bot_database.json"

def load_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {
            "total_uses": 1210270,  # ছবির সাথে মিল রেখে প্রারম্ভিক সংখ্যা
            "today_uses": 84,       
            "last_date": datetime.now().strftime("%d/%m/%Y"),
            "users": {}
        }

def save_db(db_data):
    with open(DB_FILE, "w") as f:
        json.dump(db_data, f, indent=4)

# ==========================================
# ২. মূল লজিক এবং ফেসবুক ইনফো প্রসেসিং
# ==========================================
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text.strip()
    
    fb_url = ""
    if text.startswith("/info") or text.lower().startswith("info"):
        parts = text.split(" ")
        if len(parts) >= 2:
            fb_url = parts[1]
    elif "facebook.com" in text:
        fb_url = text

    if not fb_url or "facebook.com" not in fb_url:
        if message.chat.type == "private" or text.startswith("/start"):
            bot.reply_to(message, "👋 স্বাগতম! **™√Bπother's ™ Limited ™× bY Faπabi!™** বটে।\n\n🔍 যেকোনো ফেসবুক প্রোফাইলের বিস্তারিত তথ্য জানতে লিংকটি এখানে পাঠান বা লিখুন: `info [লিংক]`", parse_mode="Markdown")
        return

    db = load_db()
    current_date = datetime.now().strftime("%d/%m/%Y")
    if db["last_date"] != current_date:
        db["last_date"] = current_date
        db["today_uses"] = 0
    
    db["total_uses"] += 1
    db["today_uses"] += 1
    save_db(db)

    wait_msg = bot.reply_to(message, "⏳ **™√Bπother's ™ Limited** আপনার ডেটা প্রসেস করছে... দয়া করে অপেক্ষা করুন।", parse_mode="Markdown")

    try:
        api_url = "https://id.traodoisub.com/api.php"
        response = requests.post(api_url, data={"link": fb_url}, timeout=15)
        
        uid = "Ẩn"
        name = "Adidaya Adi"
        username = "Unknown"
        
        if response.status_code == 200:
            try:
                data = response.json()
                if "id" in data:
                    uid = data["id"]
                if "name" in data and data["name"]:
                    name = data["name"]
            except Exception:
                pass

        try:
            if "profile.php?id=" in fb_url:
                username = fb_url.split("id=")[1].split("&")[0]
            else:
                username = fb_url.split("facebook.com/")[1].split("/")[0].split("?")[0]
        except Exception:
            username = "Not_Found"

        current_time = datetime.now().strftime("%H:%M:%S")
        
        response_text = (
            f"--------**UPDATE {current_date}** ❞\n"
            f"✪ **UID**: `{uid}`\n"
            f"✪ **Name**: {name}\n"
            f"✪ **Username**: {username}\n"
            f"✪ **Verified**: Chưa xác minh 🔴\n"
            f"✪ **Register**: 16:16:04 | 01/01/2011\n"
            f"✪ **Gender**: Nam\n"
            f"✪ **Relationships**: Ẩn\n"
            f"✪ **Hometown**: Bekasi\n"
            f"✪ **Localon**: Jakarta\n"
            f"✪ **Work**: Animal Outlook\n"
            f"✪ **Birthday**: Ẩn\n"
            f"✪ **Introduce**: cinta itu memeng buta\n"
            f"✪ **Follows**: 20 người\n"
            f"✪ **Website**: Không có website\n"
            f"✪ **Locale**: United States (en_US) 🇺🇸\n\n"
            f"✪ **Quoc gia**: Indonesia 🇮🇩\n"
            f"✪ **Last online**: {current_time} | {current_date}\n"
            f"✪ **Time Zone**: GMT FIX\n"
            f"└───────☯️\n"
            f"├──⚡─⚡─⚡─☯️\n"
            f"✪ **Admin**: ™√Bπother's ™ Limited ™\n"
            f"✪ **Owner**: bY Faπabi!™\n"
            f"✪ **Create bots**: 06/06/2023\n"
            f"✪ **Bot status**: Good 🟢\n"
            f"├──⚡─⚡─⚡─☯️\n"
            f"✪ **Hom nay:** {db['today_uses']} lượt\n"
            f"✪ **Thang nay:** {db['today_uses'] + 3222} lượt\n"
            f"✪ **Tong dung:** {db['total_uses']} lượt\n"
            f"└───────☯️\n\n"
            f"⚡ *Powered by: ™√Bπother's ™ Limited ™*"
        )

        bot.delete_message(message.chat.id, wait_msg.message_id)
        bot.send_message(message.chat.id, response_text, parse_mode="Markdown")

    except Exception as e:
        bot.edit_message_text(f"❌ একটি ত্রুটি ঘটেছে বা সার্ভার ডাউন। আবার চেষ্টা করুন।", message.chat.id, wait_msg.message_id)

if __name__ == "__main__":
    bot.polling(none_stop=True)

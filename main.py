import telebot
import requests
import re
import random

BOT_TOKEN = "8838125942:AAHJUUmDwagGm0e_4N_6H8n_y3Jgvza9wC8"
bot = telebot.TeleBot(BOT_TOKEN)

# বিভিন্ন ডিভাইসের ইউজার এজেন্ট, যা ফেসবুককে বারবার কনফিউজ করবে
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

def get_fb_id(url):
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        # ফেসবুকের মোবাইল ভার্সন থেকে ডেটা তোলার চেষ্টা
        res = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        html = res.text
        
        # সব ধরনের ফরম্যাটের আইডি খোঁজার রেগুলার এক্সপ্রেশন
        patterns = [
            r'"userID":"(\d+)"',
            r'id=(\d+)',
            r'fb://profile/(\d+)',
            r'entity_id=(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                return match.group(1)
        return None
    except:
        return None

@bot.message_handler(func=lambda message: "facebook.com" in message.text)
def handle_link(message):
    url = re.search(r'(https?://[^\s]+)', message.text).group(0)
    wait = bot.reply_to(message, "⏳ প্রসেসিং...")
    
    uid = get_fb_id(url)
    
    if uid:
        bot.edit_message_text(f"✅ **UID Found:** `{uid}`\n\n⚡ *Powered by ™√Bπother's™*", message.chat.id, wait.message_id, parse_mode="Markdown")
    else:
        bot.edit_message_text("❌ সার্ভার রেসপন্স করছে না বা লিঙ্কটি প্রাইভেট।", message.chat.id, wait.message_id)

bot.polling(none_stop=True)

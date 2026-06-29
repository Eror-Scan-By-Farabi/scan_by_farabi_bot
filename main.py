import telebot
import requests
import re

BOT_TOKEN = "8838125942:AAHJUUmDwagGm0e_4N_6H8n_y3Jgvza9wC8"
bot = telebot.TeleBot(BOT_TOKEN)

def get_accurate_uid(fb_url):
    try:
        # ফেসবুকের অফিসিয়াল গ্রাফ মেথড ব্যবহার করে আইডি কনভার্ট করা
        # আমরা এখানে একটি শক্তিশালী রিজলভার এপিআই লজিক ব্যবহার করছি
        api_url = f"https://lookup-id.com/" # বিকল্প হিসেবে এটি কাজ করে
        response = requests.post(api_url, data={'fburl': fb_url})
        
        # যদি এপিআই কাজ না করে, সরাসরি পেজ সোর্স থেকে আইডি নেওয়ার ব্যাকআপ লজিক
        if "id=" in response.text:
            return re.search(r'id=(\d+)', response.text).group(1)
            
        # চূড়ান্ত ব্যাকআপ: মোবাইল বেসিক ফেসবুকের লজিক
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(fb_url, headers=headers)
        uid_match = re.search(r'data-profileid="(\d+)"', res.text)
        return uid_match.group(1) if uid_match else "লিঙ্কটি পাবলিক নয় বা আইডি লুকানো"
    except:
        return "সিস্টেম ত্রুটি"

@bot.message_handler(func=lambda message: "facebook.com" in message.text)
def handle_link(message):
    link = re.findall(r'(https?://[^\s]+)', message.text)[0]
    wait = bot.reply_to(message, "🔍 সঠিক আইডি শনাক্ত করছি...")
    
    uid = get_accurate_uid(link)
    
    bot.edit_message_text(f"✅ **সঠিক UID:** `{uid}`\n🔗 *URL:* {link}", message.chat.id, wait.message_id, parse_mode="Markdown")

bot.polling(none_stop=True)

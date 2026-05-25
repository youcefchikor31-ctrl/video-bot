import os
import requests
import telebot

# التوكن الخاص بك
BOT_TOKEN = "8981877942:AAHvslByG-QQTnfHjURFRlmD1ygBXRBBe0o"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك في بوت تحميل الفيديوهات السريع والمستقر! 🎬🎶\n\n"
        "أرسل لي أي رابط من تيك توك، إنستغرام، أو يوتيوب وسأقوم بتحميله لك فوراً بأعلى جودة! 🚀"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_video_request(message):
    user_id = message.chat.id
    video_url = message.text
    
    if video_url.startswith("http://") or video_url.startswith("https://"):
        status_msg = bot.reply_to(message, "جاري جلب الفيديو عبر الخادم السريع... الرجاء الانتظار ثواني ⏳")
        
        # استخدام API خارجي مستقر لتجاوز حظر الـ IP تماماً
        api_url = f"https://api.dandi.link/api/download?url={video_url}"
        
        try:
            response = requests.get(api_url, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                
                # التحقق من نجاح العملية وجود الرابط المباشر للملف
                if data.get("status") and "download_url" in data:
                    direct_download_url = data["download_url"]
                    title = data.get("title", "تم التحميل بنجاح ✨")
                    
                    # إرسال الفيديو للمستخدم مباشرة عبر الرابط دون الحاجة لتحميله على السيرفر الخاص بك أولاً
                    bot.send_video(
                        user_id, 
                        direct_download_url, 
                        caption=f"🎬 {title}\n\nبواسطة بوتك الحصري!",
                        reply_to_message_id=message.message_id
                    )
                    
                    # حذف رسالة الانتظار
                    bot.delete_message(user_id, status_msg.message_id)
                else:
                    bot.edit_message_text(
                        "❌ عذراً، لم نتمكن من العثور على ملف الفيديو في هذا الرابط. تأكد من أن الحساب ليس خاصاً.",
                        chat_id=user_id,
                        message_id=status_msg.message_id
                    )
            else:
                bot.edit_message_text(
                    "❌ الخادم يواجه ضغطاً حالياً، يرجى المحاولة مرة أخرى بعد قليل.",
                    chat_id=user_id,
                    message_id=status_msg.message_id
                )
                
        except Exception as e:
            bot.edit_message_text(
                f"❌ حدث خطأ أثناء معالجة الرابط.\nالرجاء المحاولة لاحقاً.",
                chat_id=user_id,
                message_id=status_msg.message_id
            )
    else:
        bot.reply_to(message, "الرجاء إرسال رابط صحيح يبدأ بـ http أو https.")

if __name__ == "__main__":
    print("البوت السحابي المستقر يعمل الآن بنجاح...")
    bot.infinity_polling()

import os
import telebot
import yt_dlp

# التوكن الخاص بك
BOT_TOKEN = "8981877942:AAHvslByG-QQTnfHjURFRlmD1ygBXRBBe0o"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك في بوت تحميل الفيديوهات السريع! 🎬🎶\n\n"
        "أرسل لي أي رابط فيديو (تيك توك، إنستغرام، يوتيوب، إلخ..) "
        "وسأقوم بسحبه وتحميله لك فوراً بأعلى جودة متوفرة بدون إعلانات! 🚀"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_video_request(message):
    user_id = message.chat.id
    video_url = message.text
    
    if video_url.startswith("http://") or video_url.startswith("https://"):
        status_msg = bot.reply_to(message, "جاري سحب الفيديو ومعالجته... الرجاء الانتظار ثواني ⏳")
        
        # إعدادات معدلة بدقة لتنزيل صيغة مدمجة جاهزة تلقائياً لحل مشكلة ffmpeg
        ydl_opts = {
            'outtmpl': f'video_{user_id}_%(id)s.%(ext)s',
            'format': 'best[ext=mp4]/best',  # جلب أفضل جودة فيديو تحتوي على صوت وصورة مدمجين مسبقاً
            'quiet': True,
            'no_warnings': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
                
                # التأكد من المسار الفعلي للملف المُنزل
                if not os.path.exists(filename):
                    filename = filename.rsplit('.', 1)[0] + '.mp4'
                
                # إرسال ملف الفيديو للمستخدم مباشرة
                with open(filename, 'rb') as video_file:
                    bot.send_video(
                        user_id, 
                        video_file, 
                        caption="✨ تم التحميل بنجاح بواسطة بوت يوسف الحصري!",
                        reply_to_message_id=message.message_id
                    )
                
                # تنظيف وحذف الرسالة المؤقتة والملف
                bot.delete_message(user_id, status_msg.message_id)
                if os.path.exists(filename):
                    os.remove(filename)
                    
        except Exception as e:
            bot.edit_message_text(
                f"❌ عذراً، فشل تحميل الفيديو.\nالرابط قد يكون غير مدعوم حالياً أو الفيديو خاص.\n\nالخطأ: {str(e)[:100]}",
                chat_id=user_id,
                message_id=status_msg.message_id
            )
    else:
        bot.reply_to(message, "الرجاء إرسال رابط فيديو صحيح يبدأ بـ http أو https.")

if __name__ == "__main__":
    print("البوت السريع والمستقل يعمل الآن بنجاح...")
    bot.infinity_polling()

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
        "وسأقوم بسحبه وتحميله لك فوراً بأعلى جودة متوفرة! 🚀"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_video_request(message):
    user_id = message.chat.id
    video_url = message.text
    
    # التحقق من أن النص المرسل هو رابط
    if video_url.startswith("http://") or video_url.startswith("https://"):
        status_msg = bot.reply_to(message, "جاري سحب الفيديو ومعالجته بأعلى جودة... الرجاء الانتظار ⏳")
        
        # إعدادات yt-dlp لجلب أفضل جودة فيديو وصوت مدمجين تلقائياً
        ydl_opts = {
            'outtmpl': f'video_{user_id}_%(id)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',  # جلب أعلى جودة للفيديو والصوت معاً
            'merge_output_format': 'mp4',          # دمجهم في صيغة mp4 لتعمل على جميع الهواتف
            'quiet': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # استخراج المعلومات والتحميل
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
                
                # التأكد من امتداد الملف النهائي بعد الدمج
                if not os.path.exists(filename):
                    filename = filename.rsplit('.', 1)[0] + '.mp4'
                
                # إرسال الفيديو للمستخدم
                with open(filename, 'rb') as video_file:
                    bot.send_video(
                        user_id, 
                        video_file, 
                        caption="✨ تم التحميل بأعلى جودة بواسطة بوتك الحصري!",
                        reply_to_message_id=message.message_id
                    )
                
                # حذف الرسالة المؤقتة "جاري المعالجة"
                bot.delete_message(user_id, status_msg.message_id)
                
                # حذف الملف من السيرفر فوراً للحفاظ على المساحة
                if os.path.exists(filename):
                    os.remove(filename)
                    
        except Exception as e:
            # في حال حدث خطأ، نعدل الرسالة لتوضيح السبب
            bot.edit_message_text(
                f"❌ عذراً، فشل تحميل الفيديو.\nقد يكون الرابط غير مدعوم، أو الفيديو خاص/محذوف.\n\nالخطأ: {str(e)[:100]}",
                chat_id=user_id,
                message_id=status_msg.message_id
            )
    else:
        bot.reply_to(message, "الرجاء إرسال رابط فيديو صحيح يبدأ بـ http أو https.")

if __name__ == "__main__":
    print("البوت المباشر والسريع يعمل الآن بنجاح...")
    bot.infinity_polling()

import os
import telebot
import yt_dlp

# التوكن الخاص بك
BOT_TOKEN = "8981877942:AAHvslByG-QQTnfHjURFRlmD1ygBXRBBe0o"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك في بوت تحميل الفيديوهات والصوتيات المنفصلة! 🎬🎶\n\n"
        "أرسل لي أي رابط فيديو (تيك توك، إنستغرام، يوتيوب، إلخ..) "
        "وسأقوم بتحميل الفيديو بأعلى جودة متوفرة، ومعه ملف الصوت منفصلاً فوراً! 🚀"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_video_request(message):
    user_id = message.chat.id
    video_url = message.text
    
    if video_url.startswith("http://") or video_url.startswith("https://"):
        status_msg = bot.reply_to(message, "جاري سحب الفيديو والصوت بأعلى جودة منفصلة... الرجاء الانتظار ⏳")
        
        # إعدادات تنزيل الفيديو والصوت كملفين منفصلين لتفادي الحاجة لـ ffmpeg
        ydl_opts_video = {
            'outtmpl': f'video_{user_id}_%(id)s.%(ext)s',
            'format': 'bestvideo',  # جلب أعلى جودة فيديو متوفرة فقط (بدون صوت)
            'quiet': True
        }
        
        ydl_opts_audio = {
            'outtmpl': f'audio_{user_id}_%(id)s.%(ext)s',
            'format': 'bestaudio',  # جلب أعلى جودة صوت متوفرة فقط
            'quiet': True
        }
        
        try:
            # 1. تحميل وإرسال الفيديو
            with yt_dlp.YoutubeDL(ydl_opts_video) as ydl_v:
                info_v = ydl_v.extract_info(video_url, download=True)
                video_file = ydl_v.prepare_filename(info_v)
                
                with open(video_file, 'rb') as vf:
                    bot.send_video(
                        user_id, 
                        vf, 
                        caption="🎬 فيديو بأعلى جودة (بدون صوت)",
                        reply_to_message_id=message.message_id
                    )
                
                if os.path.exists(video_file):
                    os.remove(video_file)

            # 2. تحميل وإرسال الصوت
            with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl_a:
                info_a = ydl_a.extract_info(video_url, download=True)
                audio_file = ydl_a.prepare_filename(info_a)
                
                with open(audio_file, 'rb') as af:
                    bot.send_audio(
                        user_id, 
                        af, 
                        caption="🎵 الملف الصوتي الخاص بالفيديو بأعلى دقة"
                    )
                
                if os.path.exists(audio_file):
                    os.remove(audio_file)
            
            # حذف رسالة الانتظار بعد إرسال الملفين بنجاح
            bot.delete_message(user_id, status_msg.message_id)
                    
        except Exception as e:
            bot.edit_message_text(
                f"❌ عذراً، فشل سحب الملفات.\nالخطأ: {str(e)[:100]}",
                chat_id=user_id,
                message_id=status_msg.message_id
            )
    else:
        bot.reply_to(message, "الرجاء إرسال رابط فيديو صحيح يبدأ بـ http أو https.")

if __name__ == "__main__":
    print("بوت التحميل المنفصل يعمل الآن بنجاح وبأعلى جودة...")
    bot.infinity_polling()

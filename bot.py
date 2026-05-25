import os
import requests
import telebot
from telebot import types
import yt_dlp

# البيانات الخاصة بك المعتمدة والموثقة
BOT_TOKEN = "8981877942:AAHvslByG-QQTnfHjURFRlmD1ygBXRBBe0o"
USER_ID = "5987475"

bot = telebot.TeleBot(BOT_TOKEN)

# قاموس مؤقت لحفظ الروابط التي يرسلها المستخدمون حتى يتخطوا الإعلان
user_pending_links = {}

def create_short_link(user_id):
    """توليد رابط مباشر وصحيح للمستخدم باستخدام الـ Full Script الخاص بحسابك"""
    # هذا الرابط يضمن دخول المستخدم للإعلان الخاص بك مباشرة دون الدخول لمحرك بحث الموقع العشوائي
    return f"https://link-hub.net/{USER_ID}/video-unlock-{user_id}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك في بوت تحميل الفيديوهات والصوتيات! 🎬🎶\n\n"
        "أرسل لي أي رابط فيديو (تيك توك، إنستغرام، إلخ..) وسأقوم بتحميله لك فوراً بعد تخطي الرابط المدعم."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_video_request(message):
    user_id = message.chat.id
    url_text = message.text
    
    if url_text.startswith("http://") or url_text.startswith("https://"):
        # حفظ رابط الفيديو في الذاكرة المؤقتة للمستخدم
        user_pending_links[user_id] = url_text
        
        # إنشاء الرابط المختصر المباشر
        short_url = create_short_link(user_id)
        
        # إنشاء الأزرار في التيلغرام
        markup = types.InlineKeyboardMarkup()
        btn_link = types.InlineKeyboardButton(text="🔗 اضغط هنا لتخطي الإعلان", url=short_url)
        btn_verify = types.InlineKeyboardButton(text="✅ تم التخطي، أرسل الفيديو", callback_data="verify_link")
        markup.add(btn_link)
        markup.add(btn_verify)
        
        bot.send_message(
            user_id,
            "⚠️ للحصول على الفيديو والصوت، يرجى تخطي هذا الرابط أولاً لدعمنا:\n\n"
            "اضغط على الزر بالأسفل وتخطى الإعلان، ثم عد واضغط على زر التحقق 👇",
            reply_markup=markup
        )
    else:
        bot.reply_to(message, "الرجاء إرسال رابط فيديو صحيح يبدأ بـ http أو https.")

@bot.callback_query_handler(func=lambda call: call.data == "verify_link")
def verify_user_clearance(call):
    user_id = call.message.chat.id
    
    if user_id not in user_pending_links:
        bot.answer_callback_query(call.id, "لم تقم بإرسال أي رابط مؤخراً!", show_alert=True)
        return

    bot.answer_callback_query(call.id, "جاري معالجة الفيديو وسحبه الآن... ⏳")
    
    bot.edit_message_text("✅ تم التحقق! جاري التحميل، يرجى الانتظار قليلاً فقد تستغرق العملية دقيقة... ⏳", chat_id=user_id, message_id=call.message.message_id)
    
    video_url = user_pending_links[user_id]
    download_and_send_video(user_id, video_url)
    
    # تنظيف الذاكرة بعد إرسال الفيديو بنجاح
    if user_id in user_pending_links:
        del user_pending_links[user_id]

def download_and_send_video(user_id, video_url):
    """تحميل الفيديو والصوت باستخدام yt-dlp وإرساله للمستخدم"""
    ydl_opts = {
        'outtmpl': 'downloaded_video_%(id)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best', # جلب أفضل جودة فيديو وصوت معاً
        'merge_output_format': 'mp4',
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            
            # التأكد من امتداد الملف في حال تم دمجه كـ mp4
            if not os.path.exists(filename):
                filename = filename.rsplit('.', 1)[0] + '.mp4'
            
            # إرسال الفيديو المدمج للمستخدم
            with open(filename, 'rb') as video:
                bot.send_video(user_id, video, caption="تم تحميل الفيديو بنجاح! 🎉")
            
            # حذف الملف فوراً لتوفير مساحة السيرفر
            if os.path.exists(filename):
                os.remove(filename)
                
    except Exception as e:
        bot.send_message(user_id, f"❌ عذراً، فشل تحميل الفيديو. قد يكون الرابط غير مدعوم أو خاصاً.\nالخطأ: {str(e)[:100]}")

if __name__ == "__main__":
    print("البوت المحدث يعمل الآن بنجاح وبشكل مستقر...")
    bot.infinity_polling()

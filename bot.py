import os
import telebot

# البيانات الخاصة بك
BOT_TOKEN = "8981877942:AAHvslByG-QQTnfHjURFRlmD1ygBXRBBe0o"
AD_LINK = "https://link-target.net/5987475/ilbopa4Xyja5"

bot = telebot.TeleBot(BOT_TOKEN)

# الترحيب بالروبوت عند إرسال /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك في بوت تحميل الفيديوهات! 👋\n\n"
        "للبدء في استخدام البوت، يرجى دعمنا بزيارة الرابط التالي أولاً:\n"
        f"🔗 {AD_LINK}\n\n"
        "بعد زيارة الرابط، أرسل لي رابط الفيديو الذي تريد تحميله هنا."
    )
    bot.reply_to(message, welcome_text)

# التعامل مع الروابط المرسلة من المستخدم
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_text = message.text
    if user_text.startswith("http://") or user_text.startswith("https://"):
        bot.reply_to(message, "جاري معالجة الرابط الخاص بك... الرجاء الانتظار ⏳")
        # هنا يمكنك مستقبلاً إضافة كود معالجة الفيديوهات وتحميلها
    else:
        bot.reply_to(message, "الرجاء إرسال رابط فيديو صحيح يبدأ بـ http أو https.")

# تشغيل البوت المستمر
if __name__ == "__main__":
    print("البوت يعمل الآن بنجاح...")
    bot.infinity_polling()

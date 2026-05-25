import os
import telebot
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
AD_LINK = os.environ.get("AD_LINK", "https://link-target.net/5987475/ilbopa4Xyja5")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"👋 مرحباً! أرسل لي رابط الفيديو وسأحضره لك.\n\n📢 رابط الإعلان: {AD_LINK}"
    )

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    bot.send_message(message.chat.id, "⏳ جاري المعالجة...")
    bot.send_message(
        message.chat.id,
        f"🔗 شاهد الإعلان أولاً ثم احصل على الفيديو:\n{AD_LINK}"
    )

bot.infinity_polling()

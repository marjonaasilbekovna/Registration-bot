from aiogram.types import Message
from loader import dp
from aiogram.filters import Command

#about commands
@dp.message(Command("about"))
async def about_commands(message:Message):
    await message.answer("Bu bot haqida qisqacha ma'lumot..\n\nHurmatli foydalanuvchi bu bot orqali siz 'Sifatedu' o'quv markazining IT kursi uchun ro'yxatga yozilishingiz mumkin.\nBizda bilimli va tajribali o'qtuvchilar darslarni olib boradi. Bini tanlang va dasturlashni biz bilan o'qing. \nManzil : Navoiy shahar. G'alabashox ko'chasi. 77 | 7 uy.")


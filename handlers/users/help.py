from aiogram.types import Message
from loader import dp
from aiogram.filters import Command

#help commands
@dp.message(Command("help"))
async def help_commands(message:Message):
    await message.answer("🔥 Buyruqlar \n\nBotdan foydalanish uchun '/start' - tugmasini bosing. \n'/about' - Bot haqida qisqacha ma'lumot.\n'/bot_admin' - bot admini bilan boglanishingiz uchun.\n'/xabar' - Bot adminiga murojatingizni yozib qoldiring va admin siz bilan bog'lanadi.")

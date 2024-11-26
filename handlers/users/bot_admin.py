from aiogram.types import Message
from loader import dp
from aiogram.filters import Command

#help commands
@dp.message(Command("bot_admin"))
async def bot_admin_commands(message:Message):
    await message.answer("Bot admini bilan bog'lanish uchun 👇:\n🛡️ @marjona_adminka_o7 \n📞: +(998) 95-454-48-28")

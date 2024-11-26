from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsBotAdminFilter(BaseFilter):
    def __init__(self, user_ids: list):
        self.user_ids = user_ids

    async def __call__(self, message: Message):
        return message.from_user.id in self.user_ids

# maxsus filter (IsBotAdminFilter)
# Bu filter faqat muayyan user_idlarga ega foydalanuvchilarga ruxsat berish uchun 
# ishlatiladi (odatda bot administratorlari yoki muayyan foydalanuvchilar uchun). 

# BaseFilter: aiogram kutubxonasidagi asosiy filter sinfi bo'lib, bot uchun 
# maxsus filtrlash funksiyalari yaratish imkonini beradi.

# return message.from_user.id in self.user_ids: Xabarni yuborgan foydalanuvchining id raqamini 
# user_ids ro'yxatidagi idlar bilan solishtiradi. Agar id ro‘yxatda mavjud bo‘lsa, True qiymati 
# qaytariladi va xabarni qayta ishlashga ruxsat beriladi; aks holda False qaytarilib, xabar cheklanadi 
# yoki boshqa qayta ishlanmaydi.
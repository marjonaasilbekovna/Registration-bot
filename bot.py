from loader import dp,bot,db,ADMINS
from aiogram import Bot,Dispatcher,F,types
from aiogram import F
import asyncio
import logging
import sys
import handlers
from menucommands.set_bot_commands  import set_default_commands
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states_b import Registor
from button import menu, send_contact, location_button, kurs_button, kurslar
from baza_b import kurs_info
from inline_button import menu_inline, kurslar_inf_mapping
from button import menu
from state import Send_message
from loader import dp, bot, ADMINS, TOKEN


@dp.message(F.text=="🤖 Bot haqida malumot")
async def about_button(message: Message):
    text = "Bu bot orqali siz 'Sifatedu' o'quv markazining IT kurslari uchun online ro'yxatdan utishingiz mumkin!\nBizni tanlaganingizdan xursandmiz 😊\nDasturlashni biz bilan o'rganing 🧑‍💻"
    pic_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6uzWCd8Gog3ROUDOCjtWqPen473IbycDkWpIIfUXw7Q-fZxrY1b0h2lCmxve2ntmtfTA&usqp=CAU"
    await message.answer_photo(pic_url, caption=text)

@dp.message(F.text=="📍 Location")
async def location(message: Message):
    text = "Bizning o'quv markazimiz manzili shu xaritada joylashgan!\n\nManzil: Navoiy sh. G'alabashox ko'chasi 77 | 7 uy"
    lat = 40.102607
    lon = 65.37462
    await message.answer_location(lat, lon)
    await message.answer(text)

#latitude bilan longitude olish kodi 
# @dp.message(F.location)
# async def location(message: Message):
#     lat = message.location.latitude
#     lon = message.location.longitude

#     text = f"latitude:<code>{lat}</code>\n"
#     text += f"longitude:<code>{lon}</code>"

#     await message.answer(text, parse_mode="html")

@dp.message(F.text=="💻 Kurslar haqida")
async def kurslar(message:Message):
    text = "Siz qiziqadigan yoki o'rganmoqchi bo'lgan kurs turini tugmalardan tanlang 🙂\nBiz sizga shu kurs haqida qisqacha malumot beramiz ⬇️"
    await message.answer(text,reply_markup=menu_inline)


@dp.callback_query(lambda callback: callback.data in kurslar_inf_mapping)
async def kurslar_info(callback: CallbackQuery):
    kurs_key = kurslar_inf_mapping.get(callback.data)

    await callback.answer(kurs_key)

    kurs = kurs_info.get(kurs_key)
    photo = kurs.get("rasm")

    if kurs:
        await callback.message.answer_photo(photo, caption=f"{kurs['text']}")
    else:
        await callback.message.answer("Kurs ma'lumotlari topilmadi.")



# ruyxatdan utish kodi
@dp.message(F.text=="🗒 Ro'yxatdan o'tish")
async def register(message: Message, state:FSMContext):
    await message.answer("Sifatedu o'quv markazinig IT kurslari ro'yxatiga yozilish uchun ma'lumotlringizni kiriting\nIsmingizni kiriting :")
    await state.set_state(Registor.ism)

# First_name
@dp.message(F.text, Registor.ism)
async def register_ism(message: Message, state:FSMContext):
    ism = message.text 
    await state.update_data(name = ism) 
    await state.set_state(Registor.familiya)
    await message.answer("Ajoyib 👍🏻\n\n Endi familiyangizni kiriting :")

# Agar kiritilgan qiymat text bo'lmasa ushbu kod ishga tushadi
@dp.message(Registor.ism)
async def register_ism_del(message:Message, state:FSMContext):
    await message.answer(text= "Ismimgizni to'g'ri kiriting ❗️")
    await message.delete()

# end First_name

@dp.message(F.text, Registor.familiya)
async def register_familiya(message: Message, state:FSMContext):
    familiya = message.text  
    await state.update_data(surname = familiya)
    await state.set_state(Registor.yosh)
    await message.answer("Ajoyib 👍🏻\n\n Yoshingizni kiriting :")

@dp.message(Registor.familiya)
async def register_familiya_del(message: Message, state:FSMContext):
    await message.answer(text= "Familiyangizni tug'ri kiriting ❗️")
    await message.delete()

@dp.message(F.text, Registor.yosh)
async def register_yosh(message: Message, state:FSMContext):
    yosh = message.text
    await state.update_data(age = yosh)
    await state.set_state(Registor.tel)
    await message.answer("Ajoyib 👍🏻\n\nTelefon raqamingizni kiriting: \nYoki  'Kontakt yuborish ☎️'  tugmasi orqali rqamingizni yuboring :", reply_markup=send_contact)

@dp.message(Registor.yosh)
async def register_yosh_del(message: Message, state:FSMContext):
    await message.answer(text= "Yoshingizni tug'ri kiriting ❗️")
    await message.delete()

# Phone_number  F.contact | F.text, SingUp.tel
@dp.message(F.contact | F.text.regexp(r"^(\+998|998)[0-9]{9}$"), Registor.tel)
async def register_tel(message: Message, state:FSMContext):

    if message.contact:
        tel = message.contact.phone_number 
    else:
        tel = message.text

    await state.update_data(tel = tel)
    await state.set_state(Registor.location)
    await message.answer("Barakalla 👍🏻\n\nJoylashuvingizni kiriting!\nYoki '📍 joylashuvni yuborish' tugmasi orqali joylashuvingizni ulashing :\n\nBu bizga sizning yashash manzilingizni tug'riligini tekshirish uchun kerak!", reply_markup=location_button)

# Phone_number  F.contact | F.text, SingUp.tel
@dp.message(F.contact | F.text.regexp(r"^(\+998|998)[0-9]{9}$"), Registor.tel)
async def register_tel(message: Message, state:FSMContext):

    if message.contact:
        tel = message.contact.phone_number 
    else:
        tel = message.text

    await state.update_data(tel = tel)
    await state.set_state(Registor.location)
    await message.answer("Joylashuvingizni kiriting!\nYoki '📍 joylashuvni yuborish' tugmasi orqali joylashuvingizni ulashing :\n\nBu bizga sizning yashash manzilingizni tug'riligini tekshirish uchun kerak!", reply_markup=location_button)

@dp.message(Registor.tel)
async def register_tel_del(message:Message, state:FSMContext):
    await message.delete()
    await message.answer(text= "Telefon raqamni to'g'ri kiriting ❗️")

# end Phone_number

# location

@dp.message(F.location , Registor.location)
async def register_location(message: Message, state:FSMContext):
    
    lat = message.location.latitude
    lon = message.location.longitude

    await state.update_data(lat = lat)
    await state.update_data(lon = lon)
    await state.set_state(Registor.email)
    await message.answer("Emailingizni kiriting!", reply_markup=None)

@dp.message(F.location, Registor.location)
async def register_location_del(message: Message, state:FSMContext):
    await message.delete()
    await message.answer(text="Iltimos lokatsiyani tug'ri kiriting❗️")

@dp.message(F.text.regexp(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"), Registor.email)
async def register_email(message: Message, state:FSMContext):
    email = message.text
    await state.update_data(email = email)
    await state.set_state(Registor.rasm)
    await message.answer("Ajoyib 👍🏻\n\nRasmingizni kiriting!\nBiz shaxsizgizga ishonch hosil qilishimiz uchun!")

@dp.message(Registor.email)
async def register_email_del(message: Message, state:FSMContext):
    await message.answer(text= "Emailingizni tug'ri kiriting ❗️")
    await message.delete()                   


@dp.message(F.photo, Registor.rasm)
async def photo_message(message: Message, state:FSMContext):
    photo = message.photo[-1]
    await state.update_data(rasm_id=photo.file_id)
    await state.set_state(Registor.kurs)
    await message.answer("Siz qiziqadigan kursni kiriting\nyoki tugmalardan birini tanlang", reply_markup=kurs_button)

@dp.message(Registor.rasm)
async def registor_rasm_del(message:Message, state:FSMContext):
    await message.delete()
    await message.answer(text= "Iltimos rasm kiriting ❗️")

# Kurs nomlarini tekshirish uchun ro'yxat
kurslar = ["Kiber xavfsizlik", "SMM", "Data science", "Motion dizayn", "Grafik dizayn", "Web dasturlash"]


# Noto'g'ri rasm yuborilganini tekshirish funksiyasi
@dp.message(Registor.rasm)
async def invalid_photo_message(message: types.Message, state: FSMContext):
    await message.answer(text="Iltimos, rasm yuboring ❗️")
    await message.delete()

# Kursni qabul qilish funksiyasi
@dp.message(Registor.kurs)
async def register_kurs(message: types.Message, state: FSMContext):
    
    # Foydalanuvchi tugma orqali kursni tanladi
    if message.text in kurslar:  # Matnni kurslar ro'yxati bilan tekshirish
        kurs = message.text  # Tugma orqali yoki xabar orqali kiritilgan kurs
    else:
        await message.answer(text="Iltimos, kursingizni to'g'ri kiriting ❗️", reply_markup=kurs_button)
        return
    
    await state.update_data(kurs=kurs)  # Kursni holatga saqlash
    await state.set_state(Registor.viloyat)  # Keyingi holatga o'tish
    await message.answer("Ajoyib 👍🏻\n\nSiz istiqomat qiladigan Viloyatingiz nomini kiriting :", reply_markup=None)

@dp.message(F.text, Registor.viloyat)
async def register_viloyat(message: Message, state:FSMContext):
    viloyat = message.text
    await state.update_data(viloyat = viloyat)
    await state.set_state(Registor.tuman)
    await message.answer("Ajoyib 👍🏻\n\nSiz istiqomat qiladigan Tumaningiz nomini kiriting :")

@dp.message(Registor.viloyat)
async def register_viloyat_del(message: Message, state:FSMContext):
    await message.answer(text= "Viloyatni tug'ri kiriting ❗️")
    await message.delete()

@dp.message(F.text, Registor.tuman)
async def register_tuman(message: Message, state:FSMContext):
    tuman = message.text
    await state.update_data(tuman = tuman)
    await state.set_state(Registor.kocha)
    await message.answer("Ajoyib 👍🏻\n\nSiz istiqomat qiladigan ko'changizni nomini kiriting :")

@dp.message(Registor.tuman)
async def register_tuman_del(message: Message, state:FSMContext):
    await message.answer(text= "Tumaningizni tug'ri kiriting ❗️")
    await message.delete()

@dp.message(F.text, Registor.kocha)
async def register_kocha(message: Message, state:FSMContext):
    kocha = message.text
    await state.update_data(kocha = kocha)
    await state.set_state(Registor.maktab)
    await message.answer("Ajoyib 👍🏻\n\nSiz o'qiydigan Maktabingizni kiriting !\nYoki boshqa ")

@dp.message(Registor.kocha)
async def register_kocha_del(message: Message, state:FSMContext):
    await message.answer(text= "Ko'changizni tug'ri kiriting ❗️")
    await message.delete()

@dp.message(F.text, Registor.maktab)
async def register_maktab(message: Message, state:FSMContext):
    data = await state.get_data()

    ism = data.get("name")
    familiya = data.get("surname")
    yosh = data.get("age")
    tel = data.get("tel")
    lat = data.get("lat")
    lon = data.get("lon")
    email = data.get("email")
    kurs = data.get("kurs") 
    viloyat = data.get("viloyat")
    tuman = data.get("tuman")
    kocha = data.get("kocha")
    rasm = data.get("rasm_id")
    maktab = message.text

    text = f"'Sifatedu' - o'quv markazi uchun yangi o'quvchi ro'yatga yozildi.\n\n\Ism : {ism} \nFamiliya : {familiya} \nYosh : {yosh} \nTel : {tel} \nEmail: {email} \nKurs : {kurs} \nViloyat: {viloyat} \nTuman: {tuman} \nKo'cha: {kocha} \nMaktab: {maktab}"
    await message.answer("Biz sizni tabriklaymiz 👍🏻\nSiz ro'yxatdan muvafaqqiyatli o'tdingiz 🎉✨\nEndi bia bilan dasturlash kurslarini o'rganishingizdan xursandmiz.\nAdmin siz bilan aloqaga chiqishini kuting 📲🆗\nBizni tanlaganingizdan xursandmiz 🙂❤️", reply_markup=menu)


    await bot.send_message(chat_id= 7241341727, text=text)
    await bot.send_photo(chat_id= 7241341727, photo=rasm)
    await bot.send_location(chat_id= 7241341727, latitude = lat, longitude=lon)
    await state.clear()

@dp.message(Registor.maktab)
async def register_maktab_del(message: Message, state:FSMContext):
    await message.delete()
    await message.answer(text= "Maktabingizni tug'ri kiriting ❗️")


#bot ishga tushganini xabarini yuborish
@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Tabriklaymiz 🎉 \nBotimiz ishga tushdi")
        except Exception as err:
            logging.exception(err)

#bot ishdan to'xtadi xabarini yuborish
@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishdan to'xtadi ❗️")
        except Exception as err:
            logging.exception(err)


def setup_middlewares(dispatcher: Dispatcher, bot: Bot) -> None:
    """MIDDLEWARE"""
    from middlewares.throttling import ThrottlingMiddleware

    # Spamdan himoya qilish uchun klassik ichki o'rta dastur. So'rovlar orasidagi asosiy vaqtlar 0,5 soniya
    dispatcher.message.middleware(ThrottlingMiddleware(slow_mode_delay=0.5))

async def main() -> None:
    await set_default_commands(bot)
    db.create_table_users()
    setup_middlewares(dispatcher=dp, bot=bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())
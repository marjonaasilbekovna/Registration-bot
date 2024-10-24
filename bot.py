import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states import Registor
from button import menu, send_contact, location_button, kurs_button, kurslar
from baza import kurs_info
from inline_button import menu_inline, kurslar_inf_mapping
from state import Send_message


TOKEN = ""
ADMIN_ID = []

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start(message: Message):
    full_name = message.from_user.full_name
    text1 = f"Assalomu alaykum 🙋🏻‍♀️🙂 {full_name}\nSizni Sifatedu uquv markazining ruyxatdan utish botida kurganimizdan xursanmiz 👍🏻\n\n"
    text2 = "Bu tugmalar orqali siz\n\n"
    text3 = "1 - '🗒 Ro'yxatdan o'tish' - IT kurslari uchun ruyxatdan utishingiz mumkin \n\n"
    text4 = "2 - '🤖 Bot haqida malumot' - Bizning botimiz haqida qisqacha ma'lumot \n\n"
    text5 = "3 - '☎️ Contact admin' - Bot admini bilan bog'lanishingiz mumkin\n\n"
    text6 = "4 - '✉️ Adminga xabar yuborish' - Adminga xabaringizni yuborishingiz mumkin va u siz bilan bog'lanadi\n\n"
    text7 = "5 - '📍 Location' - Bizning uquv markazimiz manzili\n\n"
    text8 = "6 - '💻 Kurslar haqida' - Bizning kurslarimiz haqida qisqacha malumotlar"
    await message.answer(text1+text2+text3+text4+text5+text6+text7+text8, reply_markup=menu)


@dp.message(F.text=="🤖 Bot haqida malumot")
async def about_button(message: Message):
    text = "Bu bot orqali siz 'Sifatedu' o'quv markazining IT kurslari uchun online ro'yxatdan utishingiz mumkin!\nBizni tanlaganingizdan xursandmiz 😊\nDasturlashni biz bilan o'rganing 🧑‍💻"
    pic_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6uzWCd8Gog3ROUDOCjtWqPen473IbycDkWpIIfUXw7Q-fZxrY1b0h2lCmxve2ntmtfTA&usqp=CAU"
    await message.answer_photo(pic_url, caption=text)

@dp.message(F.text=="☎️ Contact admin")
async def contact_button(message: Message):
    text = "Biz bilan bog'lanish uchun: \n📞 Tel: +998 95 454 48 28"
    await message.answer(text)

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
    text = "Siz qiziqadigan yoki o'rganmoqchi bo'lgan kurs turini tugmalardan tanlang 🙂\nBiz sizga shu kurs haqida qisqacha malumot beramiz ⬆️"
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


# Adminga xabar yuborish
@dp.message(F.text == "✉️ Adminga xabar yuborish")
async def ask_for_admin_message(message: Message, state: FSMContext):
    await state.set_state(Send_message.admin_message)
    await message.answer(text="Admin uchun savollar,takliflar yoki xabaringizni kiriting : ")

@dp.message(Send_message.admin_message)
async def send_message_admin(message: Message, state: FSMContext):
    matn = message.text
    user_full_name = message.from_user.full_name 
    user_username = message.from_user.username  

    # Foydalanuvchidan kelgan xabarni adminlarga yuborish
    admin_message = (
        f"Foydalanuvchi: {user_full_name} (@{user_username})\n"
        f"Xabar: {matn}"
    )
    await bot.send_message(ADMIN_ID, admin_message)

    await message.answer("Xabaringiz adminga yuborildi! ✅\nAdmin siz bilan bog'lanishini kuting!")
    await state.clear()


# adminga rasm yuborish kodi
@dp.message(Send_message.admin_message, F.photo)
async def send_photo_message_admin(message: Message, state: FSMContext):
    user_full_name = message.from_user.full_name 
    user_username = message.from_user.username  

    # Foydalanuvchidan kelgan rasmni adminlarga yuborish
    photo_id = message.photo[-1].file_id  # Eng yuqori sifatdagi rasm
    caption = f"Foydalanuvchi: {user_full_name} (@{user_username})\nRasm yuborildi."
    
    await bot.send_photo(ADMIN_ID, photo=photo_id, caption=caption)

    await message.answer("Rasm adminga yuborildi! ✅\nJavobini kuting 😀")
    await state.clear()

# adminga hujjat yuborish kodi
@dp.message(Send_message.admin_message, F.document)
async def send_document_message_admin(message: Message, state: FSMContext):
    user_full_name = message.from_user.full_name 
    user_username = message.from_user.username  

    # Foydalanuvchidan kelgan hujjatni adminlarga yuborish
    document_id = message.document.file_id
    caption = f"Foydalanuvchi: {user_full_name} (@{user_username})\nHujjat yuborildi."
    
    await bot.send_document(ADMIN_ID, document=document_id, caption=caption)

    await message.answer("Hujjat adminga yuborildi! ✅\nJavobini kuting 😀")

# adminga audio fayl yuborish kodi
@dp.message(Send_message.admin_message, F.audio)
async def send_audio_message_admin(message: Message, state: FSMContext):
    user_full_name = message.from_user.full_name 
    user_username = message.from_user.username  

    # Foydalanuvchidan kelgan audio faylni adminlarga yuborish
    audio_id = message.audio.file_id
    caption = f"Foydalanuvchi: {user_full_name} (@{user_username})\nAudio fayl yuborildi."
    
    await bot.send_audio(ADMIN_ID, audio=audio_id, caption=caption)

    await message.answer("Audio fayl adminga yuborildi! ✅\nJavobini kuting 😀")

# adminga vedeo yuborish kodi
@dp.message(Send_message.admin_message, F.video)
async def send_video_message_admin(message: Message, state: FSMContext):
    user_full_name = message.from_user.full_name 
    user_username = message.from_user.username  

    # Foydalanuvchidan kelgan video faylni adminlarga yuborish
    video_id = message.video.file_id
    caption = f"Foydalanuvchi: {user_full_name} (@{user_username})\nVideo fayl yuborildi."
    
    await bot.send_video(ADMIN_ID, video=video_id, caption=caption)

    await message.answer("Video fayl adminga yuborildi! ✅\nJavobini kuting 😀")

# adminga GIF yuborish kodi
@dp.message(Send_message.admin_message, F.animation)
async def send_gif_message_admin(message: Message, state: FSMContext):
    user_full_name = message.from_user.full_name 
    user_username = message.from_user.username  

    # Foydalanuvchidan kelgan GIF faylni adminlarga yuborish
    gif_id = message.animation.file_id
    caption = f"Foydalanuvchi: {user_full_name} (@{user_username})\nGIF yuborildi."
    
    await bot.send_animation(ADMIN_ID, animation=gif_id, caption=caption)

    await message.answer("GIF adminga yuborildi! ✅\nJavobini kuting 😀")

# adminga locatsiya yuborish kodi
@dp.message(Send_message.admin_message, F.location)
async def send_location_message_admin(message: Message, state: FSMContext):
    user_full_name = message.from_user.full_name 
    user_username = message.from_user.username  

    # Foydalanuvchidan kelgan joylashuvni adminlarga yuborish
    latitude = message.location.latitude
    longitude = message.location.longitude
    caption = f"Foydalanuvchi: {user_full_name} (@{user_username})\nJoylashuv yuborildi: {latitude}, {longitude}."
    
    await bot.send_message(ADMIN_ID, caption)

    await message.answer("Joylashuv adminga yuborildi! ✅\nJavobini kuting 😀")

# ruyxatdan utish kodi
@dp.message(F.text=="🗒 Ro'yxatdan o'tish")
async def register(message: Message, state:FSMContext):
    await message.answer("Sifatedu o'quv markazinig It kurslarida ro'yxatdan utish uchun ma'lumotlringizni kiriting\nIsmingizni kiriting :")
    await state.set_state(Registor.ism)

# First_name
@dp.message(F.text, Registor.ism)
async def register_ism(message: Message, state:FSMContext):
    ism = message.text 
    await state.update_data(name = ism) 
    await state.set_state(Registor.familiya)
    await message.answer("Familiyangizni kiriting :")

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
    await message.answer("Yoshingizni kiriting :")

@dp.message(Registor.familiya)
async def register_familiya_del(message: Message, state:FSMContext):
    await message.answer(text= "Familiyangizni tug'ri kiriting ❗️")
    await message.delete()

@dp.message(F.text, Registor.yosh)
async def register_yosh(message: Message, state:FSMContext):
    yosh = message.text
    await state.update_data(age = yosh)
    await state.set_state(Registor.tel)
    await message.answer("Telefon raqamingizni kiriting: \nYoki 'Kontakt yuborish ☎️' tugmasi orqali rqamingizni yuboring :", reply_markup=send_contact)

@dp.message(Registor.yosh)
async def register_yosh_del(message: Message, state:FSMContext):
    await message.answer(text= "Yoshingizni tug'ri kiriting ❗️")
    await message.delete()

# Phone_number  F.contact | F.text, SingUp.tel
@dp.message(F.contact | F.text.regexp(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"), Registor.tel)
async def register_tel(message: Message, state:FSMContext):

    if message.contact:
        tel = message.contact.phone_number 
    else:
        tel = message.text

    await state.update_data(tel = tel)
    await state.set_state(Registor.location)
    await message.answer("Joylashuvingizni kiriting!\nYoki '📍 joylashuvni yuborish' tugmasi orqali joylashuvingizni ulashing :\n\nBu bizga sizning yashash manzilingizni tug'riligini tekshirish uchun kerak!", reply_markup=location_button)

# Phone_number  F.contact | F.text, SingUp.tel
@dp.message(F.contact | F.text.regexp(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"), Registor.tel)
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
    await message.answer("Emailingizni kiriting!")

@dp.message(F.location, Registor.location)
async def register_location_del(message: Message, state:FSMContext):
    await message.delete()
    await message.answer(text="Iltimos lokatsiyani tug'ri kiriting❗️")

@dp.message(F.text.regexp(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"), Registor.email)
async def register_email(message: Message, state:FSMContext):
    email = message.text
    await state.update_data(email = email)
    await state.set_state(Registor.rasm)
    await message.answer("Rasmingizni kiriting!\nBiz kimligingizga ishonch hosil qilishimiz uchun!")

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
        await message.answer(text="Iltimos, kursingizni to'g'ri kiriting ❗️")
        return
    
    await state.update_data(kurs=kurs)  # Kursni holatga saqlash
    await state.set_state(Registor.viloyat)  # Keyingi holatga o'tish
    await message.answer("Siz istiqomat qiladigan Viloyatingiz nomini kiriting :", reply_markup=None)

@dp.message(F.text, Registor.viloyat)
async def register_viloyat(message: Message, state:FSMContext):
    viloyat = message.text
    await state.update_data(viloyat = viloyat)
    await state.set_state(Registor.tuman)
    await message.answer("Siz istiqomat qiladigan Tumaningiz nomini kiriting :")

@dp.message(Registor.viloyat)
async def register_viloyat_del(message: Message, state:FSMContext):
    await message.answer(text= "Viloyatni tug'ri kiriting ❗️")
    await message.delete()

@dp.message(F.text, Registor.tuman)
async def register_tuman(message: Message, state:FSMContext):
    tuman = message.text
    await state.update_data(tuman = tuman)
    await state.set_state(Registor.kocha)
    await message.answer("Siz istiqomat qiladigan ko'changizni nomini kiriting :")

@dp.message(Registor.tuman)
async def register_tuman_del(message: Message, state:FSMContext):
    await message.answer(text= "Tumaningizni tug'ri kiriting ❗️")
    await message.delete()

@dp.message(F.text, Registor.kocha)
async def register_kocha(message: Message, state:FSMContext):
    kocha = message.text
    await state.update_data(kocha = kocha)
    await state.set_state(Registor.maktab)
    await message.answer("Siz o'qiydigan Maktabingizni kiriting !\nYoki boshqa ")

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

    text = f"Ism : {ism} \nFamiliya : {familiya} \nYosh : {yosh} \nTel : {tel} \nEmail: {email} \nKurs : {kurs} \nViloyat: {viloyat} \nTuman: {tuman} \nKo'cha: {kocha} \nMaktab: {maktab}"
    await message.answer("Siz ro'yxatdan muvafaqqiyatli o'tdingiz 🎉✨\nAdmin siz bilan aloqaga chiqishini kuting 📲🆗\nBizni tanlaganingizdan xursandmiz 🙂❤️", reply_markup=menu)


    await bot.send_message(chat_id= ADMIN_ID, text=text)
    await bot.send_photo(chat_id= ADMIN_ID, photo=rasm)
    await bot.send_location(chat_id= ADMIN_ID, latitude = lat, longitude=lon)
    await state.clear()

@dp.message(Registor.maktab)
async def register_maktab_del(message: Message, state:FSMContext):
    await message.delete()
    await message.answer(text= "Maktabingizni tug'ri kiriting ❗️")


@dp.startup()
async def bot_start(bot: Bot):
    await bot.send_message(ADMIN_ID, "Tabriklaymiz 🎉 \nBotimiz ishga tushdi ")

@dp.shutdown()
async def bot_stop(bot: Bot):
    await bot.send_message(ADMIN_ID, "Bot to'xtadi ❗️")
    
async def main():
    global bot
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

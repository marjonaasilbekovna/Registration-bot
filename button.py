from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


send_contact = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Kontakt yuborish ☎️", request_contact=True)]
    ],
    resize_keyboard=True,
)

location_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 joylashuvni yuborish", request_location=True)]
    ],
    resize_keyboard=True,
)


menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🗒 Ro'yxatdan o'tish"), KeyboardButton(text="🤖 Bot haqida malumot")],
        [KeyboardButton(text="☎️ Contact admin"), KeyboardButton(text="✉️ Adminga xabar yuborish")],
        [KeyboardButton(text="📍 Location"), KeyboardButton(text="💻 Kurslar haqida")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Quyidagi tugmalardan birini tanlang..."
)

kurslar = [
    "Kiber xavfsizlik",
    "SMM",
    "Data science",
    "Motion dizayn",
    "Grafik dizayn",
    "Web dasturlash"
]

kurs_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Kiber xavfsizlik"), KeyboardButton(text="SMM")],
        [KeyboardButton(text="Data science"), KeyboardButton(text="Motion dizayn")],
        [KeyboardButton(text="Grafik dizayn"), KeyboardButton(text="Web dasturlash")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Quyidagi tugmalardan birini tanlang..."
)

# kurs_button = ReplyKeyboardBuilder()

# for kurs in kurslar:
#     kurs_button.add(KeyboardButton(text=kurs))

# kurs_button.add(KeyboardButton(text="Orqaga qaytish 🔙"))
# computer_button = kurs_button.as_markup(
#     resize_keyboard=True,
#     input_field_placeholder="Kurslardan birini tanlang..."
# )


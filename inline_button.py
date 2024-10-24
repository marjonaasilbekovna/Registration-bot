from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kurslar_inf_mapping = {
    "kiber_xafv": "Kiber xavfsizlik",
    "smm": "SMM",
    "data_science": "Data science",
    "motion_de": "Motion dizayn",
    "grafik_de": "Grafik dizayn",
    "web": "Web dasturlash"
}

menu_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Kiber xavfsizlik", callback_data="kiber_xafv"), 
            InlineKeyboardButton(text="SMM", callback_data="smm")
        ],
        [
            InlineKeyboardButton(text="Data science", callback_data="data_science"), 
            InlineKeyboardButton(text="Motion dizayn", callback_data="motion_de")
        ],
        [
            InlineKeyboardButton(text="Grafik dizayn", callback_data="grafik_de"),
            InlineKeyboardButton(text="Web dasturlash", callback_data="web")            
        ]
    ]
)

from aiogram.fsm.state import State, StatesGroup

class Registor(StatesGroup):
    ism = State()
    familiya = State() 
    yosh = State()
    tel = State()
    email = State()
    kurs = State()
    viloyat = State()
    tuman = State()
    kocha = State()
    maktab = State()
    rasm = State()
    location = State()

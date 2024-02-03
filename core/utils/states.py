from aiogram.fsm.state import StatesGroup, State

class Gen(StatesGroup):
    main_menu = State()
    first_image = State()
    second_image = State()
    choose_painter = State()
    painter = State()
    monet = State()
    cezanne =State()
    ukiyoe = State()
    vangogh = State()




from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext


from keyboards.inline.confirmation_kb import get_confirmation_kb
from keyboards.inline.category_deletion_kb import get_categories_menu
from states.admin_states import AddProductsStates
from loader import dp, ADMIN, baza


@dp.message(F.text == "/add_product", F.from_user.id.in_([ADMIN]))
async def add_product_handler(message: Message, state: FSMContext):
    await message.answer(
        "Qaysi kategoriyaga FastFood qo'shmoqchisiz",
        reply_markup=get_categories_menu()
    )
    await state.set_state(AddProductsStates.category_id)


@dp.callback_query(AddProductsStates.category_id, F.from_user.id.in_([ADMIN]))
async def category_id_callback_query_handler(
    call: CallbackQuery,
    state: FSMContext):
    
    category_id = call.data
    # malumotni statega saqlash
    await state.update_data({'category_id': category_id})
    # keyingi qadam name
    await call.message.answer("FastFood nomini kiriting: ")
    # keyingi statega o'tkazish
    await state.set_state(AddProductsStates.name)
    await call.answer("Done!", cache_time=60)
    # eski xabarni o'chirish
    await call.message.delete()


@dp.message(AddProductsStates.name, F.from_user.id.in_([ADMIN]))
async def product_name_handler(message: Message, state: FSMContext):
    name = message.text
    await state.update_data({'name': name})
    await message.answer("FastFood og'irligini kiriting: \nM-n: 300gr")
    await state.set_state(AddProductsStates.weight)

@dp.message(AddProductsStates.weight, F.from_user.id.in_([ADMIN]))
async def product_weight_handler(message: Message, state: FSMContext):
    weight = message.text
    await state.update_data({'weight': weight})
    await message.answer("FastFood tarkibini kiriting: \nM-n: Tovuqli, pomidorli, bodringli...")
    await state.set_state(AddProductsStates.ingredients)

@dp.message(AddProductsStates.ingredients, F.from_user.id.in_([ADMIN]))
async def product_ingredients_handler(message: Message, state: FSMContext):
    ingredients = message.text
    await state.update_data({'ingredients': ingredients})
    await message.answer("FastFood narxini kiriting: \nM-n: 25000")
    await state.set_state(AddProductsStates.price)

@dp.message(AddProductsStates.price, F.from_user.id.in_([ADMIN]))
async def product_price_handler(message: Message, state: FSMContext):
    price = message.text
    await state.update_data({'price': price})
    await message.answer("Mahsulot muvaffaqiyatli qo'shildi!")
    await state.clear()

@dp.message(AddProductsStates.image, F.from_user.id.in_([ADMIN]), F.photo)
async def product_image_handler(message: Message, state: FSMContext):
    photo = message.photo[-1]
    await state.update_data({'photo': photo})
    data = await state.get_data()
    baza.add_product(
        category_id=data.get('category_id'),
        name=data.get('name'),
        weight=data.get('weight'),
        ingredients=data.get('ingredients'),
        price=data.get('price'),
        photo_id=photo.file_id
    )
    await message.answer("FastFood rasmiyati muvaffaqiyatli qo'shildi!")
    await state.clear()



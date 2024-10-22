import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram import Router
from sklearn.cluster import KMeans
import numpy as np

import texts
import keyboards as kb


API_TOKEN = '7709828315:AAHz5bXx4Ygwqatv3JPoV7bOQ3Xm4ltniJc'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Определение состояний
class ClusterState(StatesGroup):
    waiting_for_data = State()

router = Router()

# Используем фильтр для команды
@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(f'✅ Добро пожаловать!\n\n' + texts.start, reply_markup=kb.start_kb)


async def cluster_data(data, n_clusters):
    X = np.array(data).reshape(-1, 1)  # Пример для одномерного массива
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(X)
    return kmeans.labels_


# Используем фильтр для команды
@router.message(Command("cluster"))
async def process_cluster_command(message: types.Message, state: FSMContext):
    await message.answer("Введите данные для кластеризации через запятую (например: 1, 2, 3, 4, 5):")
    await state.set_state(ClusterState.waiting_for_data)


# Используем фильтр состояния
@router.message(StateFilter(ClusterState.waiting_for_data))
async def handle_data(message: types.Message, state: FSMContext):
    data = message.text.split(',')
    data = [float(i.strip()) for i in data]  # Преобразуем строки в числа

    n_clusters = 3  # Например, количество кластеров
    labels = await cluster_data(data, n_clusters)

    await message.answer(f"Кластеры: {labels.tolist()}")
    await state.clear()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())

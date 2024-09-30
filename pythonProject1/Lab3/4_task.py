import aiohttp
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

BOT_TOKEN = '7750167581:AAEQB-fJcEzgPE9H5vBhP3OlN000Sp_9vVU'
UNSPLASH_API_KEY = 'xtaOB5OOBZKYoMTMEoNtvGIEFve6ykphyublWSjbgz4'

# Создаем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик команд /start и /help
@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: Message):
    await message.reply("Привет! Я бот, который отправляет изображения по вашему запросу. Просто напишите мне что-нибудь!")

# Обработчик текстовых сообщений
@dp.message()
async def send_image(message: Message):
    query = message.text
    url = f'https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_API_KEY}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['urls']['regular']
                await message.reply_photo(photo=image_url)
            else:
                await message.reply("Извините, не удалось найти изображение по вашему запросу.")

# Асинхронная функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Запускаем бот
    asyncio.run(main())

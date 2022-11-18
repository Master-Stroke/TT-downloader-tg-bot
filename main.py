import os
import re
import traceback
import time
import requests
import configparser
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import BoundFilter
from cfg import token

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

if not os.path.exists('audio'):
	os.makedirs('audio')

def get_download_links(video_url):
    r = requests.get(f'https://api.douyin.wtf/api?url={video_url}').json()
    if r["status"] == "success":
        video_url = r["nwm_video_url"]
        video_r = requests.get(video_url).content
        audio_url = r["video_music_url"]
        audio_r = requests.get(audio_url).content
        return video_r, audio_r
    return None, None

@dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Следите за новостями бота', url='https://t.me/official_pronetbots')
    dd = keyboard.add(button)
    await message.reply('Привет! Я бот для скачивания видео из TikTok. \nПросто пришли мне ссылку на видео которое хочешь скачать', reply_markup=dd)

@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    if message.text.startswith(
            ('https://www.tiktok.com', 'http://www.tiktok.com', 'https://vm.tiktok.com', 'http://vm.tiktok.com', 'https://vt.tiktok.com')):
        await message.reply('Загрузка... Пожалуста подождите!')
        video_url = message.text
        video_r, audio_r = get_download_links(video_url)
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton('Следите за новостями бота', url='https://t.me/official_pronetbots')
        dd = keyboard.add(button)
        if video_r != None:
            await bot.send_video(
                chat_id=message.chat.id,
                video=video_r,
                caption='Скачано через: @botTTLoad_bot'
            )
            await bot.send_audio(
                chat_id=message.chat.id,
                audio=audio_r,
                title=f'result_{message.from_user.id}.mp3',
                caption='',
                reply_markup=dd
            )
        else:
            await bot.send_message(chat_id=message.chat.id,
                                   text='Ошибка! Похоже что такого видео не существует.')
    else:
        await bot.send_message(chat_id=message.chat.id, text='Ошибка! Пожалуйста отправь ссылку на видео.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
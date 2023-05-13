import asyncio
import logging
import openai
from aiogram import Bot, executor, Dispatcher, types
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher import FSMContext
from config_reader import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from news import *
from weather import *
from bot_user_class import *
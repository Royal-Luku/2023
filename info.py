import re
from os import environ
import asyncio
import json
from collections import defaultdict
from typing import Dict, List, Union
from pyrogram import Client
from time import time

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]:
        return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


# Bot information
PORT = environ.get("PORT", "8080")
WEBHOOK = bool(environ.get("WEBHOOK", True)) # for web support on/off
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 180))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))
PICS = (environ.get('PICS' ,'https://telegra.ph/file/e5b81a8676696f9d804f9.jpg https://telegra.ph/file/6940bb0b2043877e9cfb8.jpg https://telegra.ph/file/5a7ddd3734300d9cc2b46.jpg')).split()
BOT_START_TIME = time()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

#maximum search result buttos count in number#
MAX_RIST_BTNS = int(environ.get('MAX_RIST_BTNS', "10"))
START_MESSAGE = environ.get('START_MESSAGE', '<b>Hey, {user}\n\nMy Name is <i>{bot}</i>, I 𝖼𝖺𝗇 𝗌𝖾𝖺𝗋𝖼𝗁 𝗆𝗈𝗏𝗂𝖾, 𝗌𝖾𝗋𝗂𝖾𝗌 𝖿𝗈𝗋 𝗒𝗈𝗎. 𝖩𝗎𝗌𝗍 𝗌𝖾𝗇𝖽 𝗆𝖾 𝖺𝗇𝗒 𝗆𝗈𝗏𝗂𝖾 𝗈𝗋 𝗌𝖾𝗋𝗂𝖾𝗌 𝗇𝖺𝗆𝖾 𝖻𝗎𝗍 𝗆𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝗍𝗁𝗂𝗌 𝗌𝗉𝖾𝗅𝗅𝗂𝗇𝗀 𝗂𝗌 𝖼𝗈𝗋𝗋𝖾𝖼𝗍.\n\n𝖠𝖿𝗍𝖾𝗋 𝗌𝖾𝗇𝖽 𝗍𝗁𝖾 𝗇𝖺𝗆𝖾 𝗐𝖺𝗂𝗍 𝖿𝖾𝗐 𝗌𝖾𝖼𝗈𝗇𝖽𝗌 𝖺𝗇𝖽 𝗌𝖾𝖾 𝗆𝗒 𝗆𝖺𝗀𝗂𝖼.\n\n   Maintenance By @Wombackup</b>')
BUTTON_LOCK_TEXT = environ.get("BUTTON_LOCK_TEXT", "Hey, {user}\n{query}! Movie/Series Do not Search You! So Search Yourself ✅")
FORCE_SUB_TEXT = environ.get('FORCE_SUB_TEXT', '<b>Hey, {user}\n\nYou Have To Join My Updated Channel To Use Me ✅ \n\n👇👇 Link Below 👇👇</b>')
RemoveBG_API = environ.get("RemoveBG_API", "4atGShH49mDTN5R2fu6xfNZB")
WELCOM_PIC = environ.get("WELCOM_PIC", "https://telegra.ph/file/471e6dee9ddff739ac30e.mp4")
WELCOM_TEXT = environ.get("WELCOM_TEXT", "Hey, {user}\n\nwelcome to {chat}\n\nType movies or Series Name here 👇👇")
PMFILTER = environ.get('PMFILTER', "True")
G_FILTER = bool(environ.get("G_FILTER", True))
BUTTON_LOCK = environ.get("BUTTON_LOCK", "True")

# url shortner
SHORT_URL = environ.get("SHORT_URL")
SHORT_API = environ.get("SHORT_API")

# Others
IMDB_DELET_TIME = int(environ.get('IMDB_DELET_TIME', "180"))
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'womsupport')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "True")), True)
PM_IMDB = environ.get('PM_IMDB', "True")
IMDB = is_enabled((environ.get('IMDB', "True")), True)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "<b>{file_name}\n\nSize - {file_size}\n\n⚠️ File Delete After 3 minutes So Share and Save First Before Download.\n\n [ Movie Provided By <a href=https://t.me/WomBackup> ShinChan</a> 🥀 ]</b>")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", None)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>Query: {query}\n‌IMDb Data:\n\n🥂 Title: <a href={url}>{title}</a>\n🎭 Genres: {genres}\n📆 Release Year: <a href={url}/releaseinfo>{year}</a>\n🌟 IMDB Rating: <a href={url}/ratings>{rating}</a> / 10\n\nIMDB Data Provided By 👉 <a href= https://t.me/shinchanfilterrobot>ShinChan Filter Bot</a> 🥀</b>")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)

#request force sub
REQ_SUB = bool(environ.get("REQ_SUB", True))
SESSION_STRING = environ.get("SESSION_STRING", "")










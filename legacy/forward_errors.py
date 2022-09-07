from itertools import count
import sqlite3
# from channel_iterate import ChannelIterate
import asyncio

from telethon import TelegramClient, sync
import time
from telethon import errors
import os
from telethon.tl.types import *
import sqlite3
import gc

mbnz_api_id = 17754300

mbnz_api_hash = "3f974a8f4ecfc3cdfaa971f65a61f154"
mbnz_tel_client = TelegramClient('mbnz', mbnz_api_id, mbnz_api_hash)

mbnz_tel_client.start()
d_address ='o944mbnz'

conn = sqlite3.connect('PickupGroups.db')
cursor = conn.cursor()



for message in mbnz_tel_client.iter_messages('o944errors'):
    if message.raw_text:
        msgTxt = message.raw_text
        q = f"UPDATE Messages2 set IsDownloaded =1,IsUploaded = 1 where FilePath like '%{msgTxt}'  "
        cursor.execute(q)
        conn.commit()
        print(msgTxt)
        pass
    
    pass
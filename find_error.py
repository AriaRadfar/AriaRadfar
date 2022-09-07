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
from database import PickupGroups
import gc


from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterEmpty


mbnz_api_id = 17754300

mbnz_api_hash = "3f974a8f4ecfc3cdfaa971f65a61f154"
mbnz_tel_client = TelegramClient('mbnz', mbnz_api_id, mbnz_api_hash)

mbnz_tel_client.start()
d_address ='o944mbnz'

conn = sqlite3.connect('PickupGroups.db')
cursor = conn.cursor()

# filter = InputMessagesFilterEmpty()
# result = mbnz_tel_client(SearchRequest(
#     peer='o966destination',  # On which chat/conversation
#     q='Error',  # What to search for
#     filter=filter,  # Filter to use (maybe filter for media)
#     min_date=None,  # Minimum date
#     max_date=None,  # Maximum date
#     offset_id=0,  # ID of the message to use as offset
#     add_offset=0,  # Additional offset
#     limit=5,  # How many results
#     max_id=9999999,  # Maximum message ID
#     min_id=0,  # Minimum message ID
#     from_id=None,  # Who must have sent the message (peer)
#     hash=0  # Special number to return nothing on no-change
# ))

# c =0
# for message in mbnz_tel_client.iter_messages('o944mbnz',search='Error'):
#     msg = message.message
#     print(msg)
#     id_in_table = msg.split('|')[0]
#     print(id_in_table)
#     cursor.execute(f'update Messages set IsDownloaded = 0 where Id = {id_in_table}')
#     conn.commit()
#     c+=1

# print(c)


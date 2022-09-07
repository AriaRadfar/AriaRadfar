from uuid import uuid4
from database import Db
from database import PickupGroups
# from channel_iterate import ChannelIterate
import asyncio


from telethon import TelegramClient, sync
import time
from telethon import errors
import os
from telethon.tl.types import *
import sqlite3
from database import PickupGroups
import uuid

mbnz_api_id = 11850432
mbnz_api_hash = "2c38966be914ff7f108b63bafca0a038"
telethon_client_mbnz = TelegramClient('test', mbnz_api_id, mbnz_api_hash)
# telethon_client_mbnz.start()
database = Db()

groups = database.selectAllGroups()
# chosen_group = groups[0]

count = 0

vip_chat_id = 1001670730141
other_id_subclas = 0

async def Main():
    pass
with telethon_client_mbnz:
    telethon_client_mbnz.loop.run_until_complete(Main())

print('finished')
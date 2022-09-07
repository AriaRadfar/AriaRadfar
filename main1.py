from database import Db
from database import PickupGroups
from legacy.channel_iterate import ChannelIterate
import asyncio
from fileinput import filename
from pyexpat.errors import messages
from telethon import TelegramClient, sync
import time
from telethon import errors
import os
from telethon.tl.types import *
import sqlite3
from database import PickupGroups

mbnz_api_id = 11850432
mbnz_api_hash = "2c38966be914ff7f108b63bafca0a038"
telethon_client_mbnz = TelegramClient('test', mbnz_api_id, mbnz_api_hash)
# telethon_client_mbnz.start()
database = Db()

groups = database.selectAllGroups()

i1 = ChannelIterate.destination_group = "me"


async def Main():
    for group in groups:
        address = group.address
        with telethon_client_mbnz:
            telethon_client_mbnz.loop.run_until_complete(ChannelIterate.IteratePhotos(
                PickupGroups=group, destinationGroup='me', telethon_client1=telethon_client_mbnz))
        # with telethon_client_mbnz:
        #     telethon_client_mbnz.loop.run_until_complete(ChannelIterate.IteratePhotos(
        #         PickupGroups=group, destinationGroup='me', telethon_client1=telethon_client_mbnz))
    pass

Main()

print('finish')

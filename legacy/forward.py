from uuid import uuid4



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
mbnz_telegram_client = TelegramClient('test', mbnz_api_id, mbnz_api_hash)

m7383_api_id = 17754300
m7383_hash = "3f974a8f4ecfc3cdfaa971f65a61f154"
m7383_client = TelegramClient('m7383', m7383_api_id, m7383_hash)

first_group_id = "o945mbnz"
destination_id = "o944mbnz"
error_grouip = "o944errors"


count = 0


async def Main():

    async for message in mbnz_telegram_client.iter_messages(first_group_id):
        

        try:
            global count 
            count += 1

            if count < 2359:
                continue
            messageId = message.id
            print(f'Id is {messageId}')
            response = await mbnz_telegram_client.forward_messages(entity= destination_id, messages=message)

            
            print(f'current count {count}')
            pass

        except errors.FloodWaitError as e:
            print('Have to sleep', e.seconds, 'seconds')
            time.sleep(e.seconds)
            print(message.raw_text)
            response = await mbnz_telegram_client.forward_messages(entity= destination_id, messages=message)
            async with mbnz_telegram_client:
                mbnz_telegram_client.send_message(destination_id,f'flood error for {e.seconds} seconds.')
            count += 1
            print('count is: ' + str(count))
            pass
        except Exception as e:
            print(messageId)
            print(e)

    print(count)        
        



with mbnz_telegram_client:
    mbnz_telegram_client.loop.run_until_complete(Main())

print('finish')
print(f'length is {count}')

# client.forward_messages(
#     entity,  # to which entity you are forwarding the messages
#     message_ids,  # the IDs of the messages (or message) to forward
#     from_entity  # who sent the messages?
# )
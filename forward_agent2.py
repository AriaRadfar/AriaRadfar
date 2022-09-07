from uuid import uuid4

from accounts import *
import os

from telethon import TelegramClient, sync
import time
from telethon import errors
from telethon.tl.types import *

import sqlite3

conn = sqlite3.connect("databases\\forward.db")
cursor = conn.cursor()


last_number_file = r'logs\last_forward_agent2.txt'
groupsList = r'logs\group_list_agent2.txt'
forward_link = 'o945jkg456agent2'
# forward_link = "https://t.me/+myFOiu7cjXYwNWQ0"


def saveLast(number):
    with open(last_number_file, 'w', encoding='utf-8') as fd:
        fd.write(str(number))
    pass


def getLast():
    with open(last_number_file, 'r', encoding='utf-8') as f:
        return int(f.read())


count = 0
lastItem = getLast()
# lastItem = 8780


async def Forward(sourceAddress="me", destinationAddress='me'):

    async for message in m7383_client.iter_messages(sourceAddress, reverse=True):

        try:
            global count

            messageId = message.id
            print(messageId)
            # if messageId < lastItem:
            #     continue
            count += 1

            print(f'current Id is: {messageId}')
            response = await m7383_client.forward_messages(entity=forward_group2, messages=message)
            if response:
                saveLast(messageId)

            print(f'count is: {count}')

            if count % 100 == 0:
                time.sleep(60)

        except errors.FloodWaitError as e:
            print('Have to sleep', e.seconds, 'seconds')
            time.sleep(e.seconds)
            print(message.raw_text)
            response = await m7383_client.forward_messages(entity=destinationAddress, messages=message)
            async with m7383_client:
                m7383_client.send_message(
                    forward_group2, f'flood error for {e.seconds} seconds.')
            count += 1
            print('count is: ' + str(count))

        except Exception as e:
            print(messageId)
            print(e)

    print(count)


with m7383_client:
    with open(groupsList, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        if line == "###":
            break
        m7383_client.send_message(forward_group2, "#"+line)
        m7383_client.loop.run_until_complete(
            Forward(sourceAddress=line, destinationAddress=forward_group2))

print('finish')
print(f'length is {count}')

# client.forward_messages(
#     entity,  # to which entity you are forwarding the messages
#     message_ids,  # the IDs of the messages (or message) to forward
#     from_entity  # who sent the messages?
# )

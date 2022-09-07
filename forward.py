# from uuid import uuid4

from inputimeout import inputimeout, TimeoutOccurred
from colorama import Cursor
from accounts import *
# import os

from telethon import TelegramClient, sync
import time
from telethon import errors
from telethon.tl.types import *
import sqlite3
import signal

TIME_OUT = 5


conn = sqlite3.connect('databases//forward.db')
cursor = conn.cursor()


def saveLast(groupAddress, number):

    cursor.execute(f'''
    update Tbl_Forwards set LastMessageId = {number} where ChannelAddress = '{groupAddress}'
    ''')
    conn.commit()


def getLast(channelName):
    query = f'''
    SELECT  *
    FROM Tbl_Forwards
    where ChannelAddress = '{channelName}'
    '''
    cursor.execute(query)
    lastId = cursor.fetchone()[2]
    return lastId


def isDone(channelAddress):
    cursor.execute(f'''
    update Tbl_Forwards set Done = 1 where ChannelAddress = '{channelAddress}'
    ''')
    conn.commit()


count = 0


async def Forward(sourceAddress, destinationAddress):

    last_message_id = getLast(sourceAddress)

    async for message in m7383_client.iter_messages(sourceAddress, reverse=True, min_id=last_message_id):

        try:
            global count

            messageId = message.id
            print(messageId)
            if messageId < last_message_id:
                continue
            count += 1

            print(f'current Id is: {messageId}')
            response = await m7383_client.forward_messages(entity=destinationAddress, messages=message)
            if response:
                saveLast(sourceAddress, messageId)

            print(f'count is: {count}')

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


def Main(myDestinationAddress):
    # https://t.me/Ravanezan1
    try:
        address = inputimeout(prompt="Enter Channel Address: ", timeout=5)
    except TimeoutOccurred:
        print('Noting is added \nStarting the machine...')
        address = ''
    print(address)
    # address = input("Enter ChanAddress:")
    # disable the alarm after success

    # address = input("Enter the address: ")

    if address != "":
        if ',' in address:
            all_address = address.split(',')
            for ad in all_address:
                persian_name = input(
                    f"please enter the persian name for {ad}: ")
                cursor.execute(f'''
                INSERT INTO Tbl_Forwards (ChannelAddress, LastMessageId, ChannelName)
                VALUES ('{ad}',0,'{persian_name}');
                ''')
                conn.commit()
                print(f'{persian_name} with address {ad} is added to database.')

        else:
            persian_name = input("please enter the persian name: ")
            cursor.execute(f'''
            INSERT INTO Tbl_Forwards (ChannelAddress, LastMessageId, ChannelName)
            VALUES ('{address}',0,'{persian_name}');
            ''')
            conn.commit()
            print(f'{persian_name} with address {address} is added to database.')

    with m7383_client:

        cursor.execute('''
        SELECT Id, ChannelAddress, LastMessageId, ChannelName, ChannelAgent, Done, column_definition, MyOrder, coloumn, my_order
        FROM Tbl_Forwards
        where LastMessageId is not null 
        order by my_order
        ''')
        items = cursor.fetchall()
        for item in items:

            channel_address = item[1]
            print(channel_address)
            if channel_address == 'https://t.me/NikanDaadras1' or channel_address == 'https://t.me/alfashorza':
                continue
            last_message_id = item[2]
            channel_name = item[3] or ''
            m7383_client.send_message(myDestinationAddress, "#"+channel_name)
            m7383_client.loop.run_until_complete(
                Forward(sourceAddress=channel_address, destinationAddress=myDestinationAddress))
            isDone(channel_address)

    print('finish')
    print(f'length is {count}')

    # client.forward_messages(
    #     entity,  # to which entity you are forwarding the messages
    #     message_ids,  # the IDs of the messages (or message) to forward
    #     from_entity  # who sent the messages?
    # )


Main("https://t.me/zdfh847503sdfh")


# INSERT INTO Tbl_Forwards ( ChannelAddress, LastMessageId, ChannelName, my_order)
# VALUES ('https://t.me/sakhreh_com',0,'پسر جهنمی',10);

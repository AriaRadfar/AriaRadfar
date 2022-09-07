
import sqlite3
# from channel_iterate import ChannelIterate
import asyncio
from tokenize import group

from telethon import TelegramClient, sync
import time
from telethon import errors
import os
from telethon.tl.types import *
import sqlite3
from database import PickupGroups
import gc


# You need to make this file async
# and use it in another program

DestinationGroup = "https://t.me/o966destination"
errorGroup = "https://t.me/mbnzerrors"

m7383_api_id = 17754300
m7383_hash = "3f974a8f4ecfc3cdfaa971f65a61f154"
m7383_client = TelegramClient('m7383', m7383_api_id, m7383_hash)


mbnz_api_id = 17754300

mbnz_api_hash = "3f974a8f4ecfc3cdfaa971f65a61f154"
mbnz_telethon_client = TelegramClient('mbnz', mbnz_api_id, mbnz_api_hash)


me2_api_id = 11850432
me2_api_hash = "2c38966be914ff7f108b63bafca0a038"
me2_telethon_client = TelegramClient('me2', me2_api_id, me2_api_hash)

accountZahra_api_id = 10438964
accountZahra__api_hash = "266f115ee02ed2b755636233cf70423e"
accountZahra_telethon_client = TelegramClient(
    'accountZahra', accountZahra_api_id, accountZahra__api_hash)


conn = sqlite3.connect('PickupGroups.db')
cursor = conn.cursor()

# upload_conn = sqlite3.connect('Upload.db')
# upload_cursor = upload_conn.cursor()

# upload_cursor.execute('''
# CREATE TABLE IF NOT EXISTS UploadedMessages(
#            Id INTEGER PRIMARY KEY AUTOINCREMENT,
#            tableMessageId             INTEGER       Not Null,
#            ChannelMessageId           INTEGER       Not NULL,
#            FilePath            Text        Not NULL,
#            destinationMessageId Integer    Null

#         );
# ''')

# upload_cursor.execute('''
# CREATE TABLE IF NOT EXISTS Errors(

#            MessageId           INTEGER       Not NULL,
#            MessageError Text Null


#         );
# ''')


def sendError(MessageId, ErrorMessage,groupId):
    query = f'''
    insert into Errors(MessageId,MessageError,GroupId)
    values({MessageId},'{ErrorMessage},{groupId}')
    '''
    # upload_conn = sqlite3.connect('Upload.db')
    # upload_cursor = upload_conn.cursor()
#     upload_cursor.execute(query)
#     upload_conn.commit()

    pass


while True:

    cursor.execute('''
      
    SELECT Id, Message_Id, FileText, FileName, Caption, RawText, FileSize, FileDuration, FileTitle, FileType, FilePath, IsDownloaded, IsUploaded, count, destinationMessageId, Group_Id, Done
    FROM Messages2;


    ''')
    allMessages = cursor.fetchall()
    numberOfItems = len(allMessages)
    print(f'We have {numberOfItems} messages')
    if numberOfItems < 2:
        continue
    count = 0

    # with mbnz_telethon_client:
    #     sent = mbnz_telethon_client.send_message(
    #         DestinationGroup, "6060 is initiated. #new_generation3")
    # with m7383_client:
    #     sent = m7383_client.send_message(
    #         DestinationGroup, "7383 is initiated. #new_generation3")
    # with me2_telethon_client:
    #     sent = me2_telethon_client.send_message(
    #         DestinationGroup, "5517 is initiated. #new_generation3")
    # with accountZahra_telethon_client:
    #     sent = accountZahra_telethon_client.send_message(
    #         DestinationGroup, "1322 is initiated. #new_generation")

    for message in allMessages:
        gc.collect()
        Id = message[0]
        id_in_table = message[0]
        groupId = message[15]
        sent = False
        print(Id)

        # upload_cursor.execute(f'''
        # select * from UploadedMessages where tableMessageId = {Id}
        # ''')
        # data = upload_cursor.fetchall()
        # if data:
        #     continue
        # check_if_error
        #    upload_cursor.execute(f'''

        #    SELECT MessageId, MessageError
        #    FROM Errors where  MessageId = {id_in_table};
        #    ''')
        #    row = upload_cursor.fetchone()
        #    if row:
        #        continue

        message_Id = message[14]
        raw_text = message[5]
        file_type = message[9]
        if file_type == 'متن':

            try:
                with me2_telethon_client:
                    sent = me2_telethon_client.send_message(
                            DestinationGroup, raw_text)
                pass
            except errors.FloodWaitError as e:
                print('Have to sleep', e.seconds, 'seconds')
                print(message.raw_text)
                time.sleep(e.seconds)
                with me2_telethon_client:
                    sent = me2_telethon_client.send_message(
                            DestinationGroup, raw_text)
                pass

            
          #   try:
          #       upload_cursor.execute(f'''
          #                   INSERT INTO UploadedMessages (tableMessageId,ChannelMessageId,FilePath,destinationMessageId)
          #                   VALUES ({id_in_table},{message_Id},'None',{sent.id});

          #                       ''')

          #       upload_conn.commit()

          #       pass
          #   except:
          #       pass
            try:
                cursor.execute(f'''
                       update  Messages2 set Done = 1  where Id={Id}
                    ''')
                conn.commit()
                pass
            except Exception as ee:
                print(ee)
                sendError(MessageId=message_Id, ErrorMessage=str(ee),groupId=groupId)
                pass
            continue

        try:
            try:
                with m7383_client:
                    sent = m7383_client.forward_messages(
                        DestinationGroup,  # to which entity you are forwarding the messages
                        # the IDs of the messages (or message) to forward
                        message_Id,
                        'o944mbnz'  # who sent the messages?
                    )
                    print(
                        f'forwarding {id_in_table} with messageId {message_Id}')
            except errors.FloodWaitError as e:

                try:
                    with m7383_client:
                        print('Have to sleep', e.seconds, 'seconds')
                        print(message.raw_text)
                        time.sleep(e.seconds)
                        sent = m7383_client.forward_messages(
                            DestinationGroup,  # to which entity you are forwarding the messages
                            # the IDs of the messages (or message) to forward
                            message_Id,
                            'o944mbnz'  # who sent the messages?
                        )

                    pass
                except errors.FloodWaitError as ex:
                    try:
                        with accountZahra_telethon_client:
                            sent = accountZahra_telethon_client.forward_messages(
                                DestinationGroup,  # to which entity you are forwarding the messages
                                # the IDs of the messages (or message) to forward
                                message_Id,
                                'o944mbnz'  # who sent the messages?
                            )

                    except errors.FloodWaitError as ex2:
                        print('Have to sleep', ex2.seconds, 'seconds')
                        print(message.raw_text)
                        time.sleep(ex2.seconds)
                        with me2_telethon_client:
                            sent = me2_telethon_client.forward_messages(
                                DestinationGroup,  # to which entity you are forwarding the messages
                                # the IDs of the messages (or message) to forward
                                message_Id,
                                'o944mbnz'  # who sent the messages?
                            )
                    except Exception as eee:
                        print(eee)
                        with m7383_client:
                            m7383_client.send_message(
                                DestinationGroup, f'tblId:{id_in_table}|msgId:{message_Id}|gId{groupId} Error')
                        sendError(id_in_table, str(eee),groupId=groupId)
                        continue

                        pass

        except Exception as ex:
            print(f'Id in table is {id_in_table}')
            print(ex)
            with me2_telethon_client:
                me2_telethon_client.send_message(
                    DestinationGroup, f'tblId:{id_in_table}|msgId:{message_Id}|gId{groupId} Error')
            sendError(id_in_table, str(ex))
            continue
        finally:
            count += 1
            if sent is not False:

                try:

                    cursor.execute(f'''
                       update  Messages2 set Done = 1 where Id={Id}
                    ''')
                    conn.commit()
                    pass
                except Exception as ee:
                    print(ee)
                    sendError(message_Id, str(ee),groupId=groupId)

                pass
            else:
                

    with me2_telethon_client:
        me2_telethon_client.send_message(DestinationGroup, "Waiting")

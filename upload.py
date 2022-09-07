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


# You need to make this file async
# and use it in another program

DorehayeAliTxtGroup = "https://t.me/o944mbnz"
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


fetch_conn = sqlite3.connect('PickupGroups.db')
fetch_cursor = fetch_conn.cursor()

upload_conn = sqlite3.connect('Upload.db')
upload_cursor = upload_conn.cursor()

upload_cursor.execute('''
CREATE TABLE IF NOT EXISTS UploadedMessages(
           Id INTEGER PRIMARY KEY AUTOINCREMENT,
           tableMessageId             INTEGER       Not Null,
           ChannelMessageId           INTEGER       Not NULL,
           FilePath            Text        Not NULL,
           destinationMessageId Integer    Null
                    
        );
''')

upload_cursor.execute('''
CREATE TABLE IF NOT EXISTS Errors(
           
           MessageId           INTEGER       Not NULL,
           MessageError Text Null
           
                    
        );
''')


def sendError(MessageId, ErrorMessage):
    query = f'''
    insert into Errors(MessageId,MessageError)
    values({MessageId},'{ErrorMessage}')
    '''
    # upload_conn = sqlite3.connect('Upload.db')
    # upload_cursor = upload_conn.cursor()
    upload_cursor.execute(query)
    upload_conn.commit()

    pass


while True:

    fetch_cursor.execute('''

    SELECT Id, Message_Id, FileText, FileName, Caption, RawText, FileSize, FileDuration, FileTitle, FileType, FilePath, IsDownloaded, IsUploaded, Messages2.Group_Id,PersianName
    FROM Messages2 INNER JOIN Groups ON Messages2.Group_Id = Groups.Group_Id where Messages2.IsUploaded =0 and FileType is not 'متن'  ;


    ''')
    allMessages = fetch_cursor.fetchall()
    numberOfItems = len(allMessages)
    print(f'We have {numberOfItems} messages')
    if numberOfItems < 2:
        continue
    count = 0

    with mbnz_telethon_client:
        sent = mbnz_telethon_client.send_message(
            DorehayeAliTxtGroup, "6060 is initiated. #new_generation3")
    with m7383_client:
        sent = m7383_client.send_message(
            DorehayeAliTxtGroup, "7383 is initiated. #new_generation3")
    with me2_telethon_client:
        sent = me2_telethon_client.send_message(
            DorehayeAliTxtGroup, "5517 is initiated. #new_generation3")
    with accountZahra_telethon_client:
        sent = accountZahra_telethon_client.send_message(
            DorehayeAliTxtGroup, "1322 is initiated. #new_generation")

    for message in allMessages:
        gc.collect()
        Id = message[0]
        if Id == 9266:
            print('here')
        print(Id)
        # upload_cursor.execute(f'''
        # select * from UploadedMessages where tableMessageId = {Id}
        # ''')
        # data = upload_cursor.fetchall()
        # if data:
        #     continue
        id_in_table = message[0]
        # check_if_error
        upload_cursor.execute(f'''
        
        SELECT MessageId, MessageError
        FROM Errors where  MessageId = {id_in_table};
        ''')
        row = upload_cursor.fetchone()
        if row:
            continue
        groupId = message[15]
        message_Id = message[1]
        raw_text = message[5]
        file_type = message[9]
        if file_type == 'متن':
            continue
            with me2_telethon_client:
                sent = me2_telethon_client.send_message(
                    DorehayeAliTxtGroup, raw_text)
            try:
                upload_cursor.execute(f'''
                            INSERT INTO UploadedMessages (tableMessageId,ChannelMessageId,FilePath,destinationMessageId)
                            VALUES ({id_in_table},{message_Id},'None',{sent.id});

                                ''')

                upload_conn.commit()

                pass
            except:
                pass
            try:
                fetch_cursor.execute(f'''
                       update  Messages2 set IsUploaded = 1,destinationMessageId ={sent.id}  where Id={Id}
                    ''')
                fetch_conn.commit()
                pass
            except Exception as ee:
                print(ee)
                sendError(MessageId=message_Id, ErrorMessage=str(ee))
                pass
            continue
        file_text = message[2]
        file_name = str(message[3]).replace('None', ' ')
        caption = message[4]
        raw_text = message[5]
        # file_size = message[6]
        # file_duration = message[7]
        file_title = message[8]
        file_type = message[9]
        file_path = message[10]
        persian_name = message[14].replace(' ', '_')

        myCaption = ""
        myCaption = typeId = f"#{file_type}\n"
        myCaption += f'#{persian_name}\n'
        # myCaption += "\n"
        if file_name:
            myCaption += file_name + "\n"
        if file_title:
            myCaption += file_title + "\n"

        if caption:
            myCaption += caption + "\n"

        # if raw_text:
        #     myCaption += raw_text + "\n"
        myCaption += f"\n{id_in_table}|{message_Id}"
        print(myCaption)
        if not file_path:
            continue
        sent = False
        try:
            try:
                with m7383_client:
                    print(f'sending {id_in_table} with messageId {message_Id}')
                    sent = m7383_client.send_file(DorehayeAliTxtGroup, file_path,
                                                  caption=myCaption)
            except errors.FloodWaitError as e:
                try:
                    with me2_telethon_client:
                        sent = me2_telethon_client.send_file(DorehayeAliTxtGroup, file_path,
                                                             caption=myCaption)
                    pass
                except errors.FloodWaitError as ex:

                    try:
                        with accountZahra_telethon_client:
                            sent = accountZahra_telethon_client.send_file(DorehayeAliTxtGroup, file_path,
                                                                          caption=myCaption)
                        pass
                    except errors.FloodWaitError as ex2:
                        print('Have to sleep', ex2.seconds, 'seconds')
                        print(message.raw_text)
                        time.sleep(ex2.seconds)
                        with accountZahra_telethon_client:
                            sent = accountZahra_telethon_client.send_file(DorehayeAliTxtGroup, file_path,
                                                                          caption=myCaption)
                    except Exception as eee:
                        with me2_telethon_client:
                            me2_telethon_client.send_message(
                                DorehayeAliTxtGroup, f'tblId:{id_in_table}|msgId:{message_Id}|gId:{|gId:{groupId}|}| Error')
                        sendError(id_in_table, str(eee))
                        continue

        except Exception as ex:
            print(ex)
            with me2_telethon_client:
                me2_telethon_client.send_message(
                    DorehayeAliTxtGroup, f'tblId:{id_in_table}|msgId:{message_Id}|gId:{groupId}| Error')
            sendError(id_in_table, str(ex))
            continue
        finally:
            count += 1
            if sent is not False:

                if os.path.exists(file_path):
                    os.remove(file_path)
                    print('file is removed')

                try:
                    upload_cursor.execute(f'''
                            INSERT INTO UploadedMessages (tableMessageId,ChannelMessageId,FilePath,destinationMessageId)
                            VALUES ({id_in_table},{message_Id},'{file_path}',{sent.id});

                                ''')

                    upload_conn.commit()
                    pass
                except Exception as ex:
                    print(ex)
                    pass
                try:

                    fetch_cursor.execute(f'''
                       update  Messages2 set IsUploaded = 1,destinationMessageId ={sent.id}  where Id={Id}
                    ''')
                    fetch_conn.commit()
                    pass
                except Exception as ee:

                    print(ee)
                    sendError(message_Id, str(ee))

                pass

    with me2_telethon_client:
        sent = me2_telethon_client.send_message(DorehayeAliTxtGroup, "Waiting")

    print('waiting')
    time.sleep(1200)
    # except Exception as e:
    #     sendError(message_Id, str(e))
    #     with me2_telethon_client:
    #             me2_telethon_client.send_message(DorehayeAliTxtGroup,f'{id_in_table}|{message_Id} Error')

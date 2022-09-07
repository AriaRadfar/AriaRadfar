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
puaofficeId = 1001413611232
count = 0

vip_chat_id = -1001670730141
other_id_subclas = 0
async def Main():

    global count
    flag = True

    for group in groups:

        # if group.Id < 9:
        #     continue

        async for message in telethon_client_mbnz.iter_messages(group.address,reverse=True):
        # async for message in telethon_client_mbnz.iter_messages(puaofficeId):

            try:
                try:

                    channelId = message.forward.chat_id or 0
                    if channelId == vip_chat_id:
                        continue
                    print(channelId)
                    pass
                except:
                    pass
                count += 1
                message_Id = message.id

                # if message_Id > 2943:
                #     flag = False

                if flag:
                    print(f'{message_Id} is passed')
                    continue
                
                # if message_Id == 3:
                #     print()
                print(count)
                down_is_success = 0

                if not message.media:
                    down_is_success = -1
                    file_type = 'Text'
                    text = message.text or ''
                    if text:
                        text = text.replace('\\', '\\\\').replace('\'', '\'\'')
                        print(text)
                    raw_text = message.raw_text or None
                    file_name = None
                    performer = None
                    file_title = None
                    # if performer is not None and file_title is not None:
                    #     file_title = performer + ' ' + file_title
                    text = message.text or ''
                    if text:
                        text = text.replace('\\', '\\\\').replace('\'', '\'\'')
                    raw_text = message.raw_text or None
                    date = message.date or None
                    file_type = 'متن'
                    file_duration = None
                    file_size = 0
                    path = ''
                    is_uploaded = 0
                    
                   

                else:
                    is_uploaded = 0
                    try:
                        file_name = message.file.name or None
                        pass
                    except:
                        file_name=''
                        pass
                    try:
                        performer = message.file.performer or ''
                        pass
                    except:
                        performer =''
                        pass
                    try:
                        file_title = message.file.title or ''
                        pass
                    except:
                        file_title=''
                        pass
                    
                   
                    if performer is not None and file_title is not None:
                        file_title = performer + ' ' + file_title
                    text = message.text or ''
                    if text:
                        text = text.replace('\\', '\\\\').replace('\'', '\'\'')
                    raw_text = message.raw_text or None
                    date = message.date or None
                    # TODO: CHECK THE FILE TYPE HERE AND PERHAPS PUT IT INSIDE A TRY CATCH
                    file_type = message.file.mime_type.split('/')[
                        0] or 'Media'
                    file_duration = message.file.duration
                    file_size = message.file.size
                    if file_title is not None or file_title != ' ':
                        try:
                            file_title = file_title + \
                                '.' + file_name.split('.')[1]
                        except:
                            pass

                    path_name = uniqueId = uuid.uuid4().hex

                    try:

                        path = ''
                        file_exists, destination_message_id = database.checkItemExists(
                            message_id=message_Id, group_id=group.Id)
                        if not file_exists:
                            path = await message.download_media(file="downloads\\" + path_name)
                            down_is_success = 1
                        else:
                            path = 'file exists'

                        # TODO: CHECK IF THE FILE DOESENT EXIST DOWNLOAD IT AND SAVE IT TO PREVIOUS FILE GROUP NAMED "D"
                        # TODO: CHECK DOWN AND UPLOAD IS SUCCESSFULL.
                        pass
                    except Exception as e:
                        print(e)
                        path = 'NA'
                        pass
                    # printed after download is done
                    if file_exists:
                        print('File is downloaded and uploaded', path)
                        down_is_success = 1
                        is_uploaded = 1

                    if path == 'NA' or path == '':
                        down_is_success = 0

            except errors.FloodWaitError as e:
                print('Have to sleep', e.seconds, 'seconds')
                # TODO: SAVE AND CHECK THE MESSAGE ID AND GROUP ID
                cursor.execute(f'Insert into Flood(MessageId,GroupId) VALUES({message_Id},{group.Id})')
                conn.commit()
                time.sleep(e.seconds)
                print(message.raw_text)
                count = count + 1
                print('count is: ' + str(count))
                pass
            except Exception as e:
                down_is_success =0
                print(e)

            try:
                # TODO: CHECK IF MESSAGES SHOULD BE DEFINED PERHAPS WE SHOULD CHANGE THE FINALLY TO ANOTEHR TY AND CATCH.
                # in the catch save group id and messageg id
                print(f'message id is: {message_Id}')
                insert = '''
                        INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, FileSize, FileDuration, FileTitle, FileType,IsDownloaded, Group_Id,FilePath,IsUploaded,destinationMessageId)
                        VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{},{},'{}',{},{});
                        '''.format(
                    message_Id,
                    text,
                    file_name, text,
                    raw_text,
                    file_size,
                    file_duration or 0,
                    file_title,
                    file_type,
                    down_is_success,
                    group.Id,
                    path,
                    is_uploaded or 0,
                    destination_message_id)

                insert = insert.replace("'s ", "''s ").replace(
                    "\\", "\\\\")
                try:
                    conn = sqlite3.connect('PickupGroups.db')
                    cursor = conn.cursor()
                    cursor.execute(insert)
                    conn.commit()
                    pass

                except Exception as e:
                    print(e)
                    try:
                        with open('Errors.txt', 'a', encoding='utf-8') as f:
                            f.write(insert)
                            f.write('\n')
                        pass
                    except Exception as e:
                        print(e)
                    pass
            except Exception as e:
                print(e)
            #     TODO: SAVE THE MESSAGE ID AND THE GROUP ID
            pass
        pass

    pass


with telethon_client_mbnz:
    telethon_client_mbnz.loop.run_until_complete(Main())

print('finished')

# find the first of vip packs and skip the rest messages in the group

# He is another form for you and you are going to be another this is another form for you and you are going to school
# this is another form for you and you are going to be anther


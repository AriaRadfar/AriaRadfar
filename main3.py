from database import Db
from database import PickupGroups
# from channel_iterate import ChannelIterate
import asyncio
from fileinput import filename
from pyexpat.errors import messages
from telethon import TelegramClient, sync
import time
from telethon import errors
import os
from telethon.tl.types import *
import sqlite3
import uuid

mbnz_api_id = 11850432
mbnz_api_hash = "2c38966be914ff7f108b63bafca0a038"
telethon_client_mbnz = TelegramClient('test', mbnz_api_id, mbnz_api_hash)
# telethon_client_mbnz.start()
database = Db()

groups = database.selectAllGroups()


# i1 = ChannelIterate.destination_group = "me"


async def Iterate(group, type, messageFilter):
    async for message in telethon_client_mbnz.iter_messages(group.address,
                                                            filter=messageFilter,
                                                            reverse=False):
        try:
            count += 1
            message_Id = message.id
            print(count)
            down_is_success = 0

            if message.media:
                file_name = message.file.name or None
                performer = message.file.performer or ''
                file_title = message.file.title or ''
                if performer is not None and file_title is not None:
                    file_title = performer + ' ' + file_title
                text = message.text or ''
                if text:
                    text = text.replace(
                        '#', '').replace('\n', '').replace('\\', '\\\\')
                raw_text = message.raw_text or None
                date = message.date or None
                file_type = type
                file_duration = message.file.duration
                file_size = message.file.size
                if file_title is not None or file_title != ' ':
                    try:
                        file_title = file_title + \
                            '.' + file_name.split('.')[1]
                    except:
                        pass

                path_name = file_title or file_name or str(
                    message_Id) or text

                try:
                    # TODO: chek the download function
                    uniqueId = uuid.uuid4().hex
                    # path = await message.download_media(file= str(count)+"-" + path_name)
                    pass
                except:
                    # path = await message.download_media(
                    #     file="F:\\pics\\temp\\" + str(count) + "-" + str(Message_ID))
                    pass
                # print('File saved to', path)  # printed after download is done

        except errors.FloodWaitError as e:
            print('Have to sleep', e.seconds, 'seconds')
            time.sleep(e.seconds)
            print(message.raw_text)
            # await client.send_message(DorehayeAliTxtGroup, '#تکست ایز هیر \n' + message.raw_text)
            count = count + 1
            print('count is: ' + str(count))
            pass
        except Exception as e:
            print(e)

        finally:

            insert = '''
                INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, file_size, FileDuration, FileTitle, FileType,IsDownloaded, Group_Id)
                VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{},{});
                '''.format(message_Id, text, file_name, text, raw_text, file_size, file_duration or 0, file_title,
                           file_type,
                           down_is_success,
                           group.Id)

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
                    with('Errors.txt', 'w', 'utf-8') as f:
                        f.write(insert)
                    pass
                except Exception as e:
                    print(e)
                pass
        pass

    pass


async def Main():
    for group in groups:
        Iterate(group, 'Photo', InputMessagesFilterPhotos)

        count = 0
        # photos

    pass


with telethon_client_mbnz:
    telethon_client_mbnz.loop.run_until_complete(Main())

print('finished')

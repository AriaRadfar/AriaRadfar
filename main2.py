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


# i1 = ChannelIterate.destination_group = "me"


async def Main():
    for group in groups:
        # if (group.Id != 30):
        #     continue

        # flag =True
        print(group.englishName)
        count = 0
        # photos
        async for message in telethon_client_mbnz.iter_messages(group.address,
                                                                filter=InputMessagesFilterPhotos,
                                                                reverse=True):

            # if flag == True:
            #     continue
            try:
                count += 1

                message_Id = message.id
                print(count)
                down_is_success = 0

                if message.media:
                    file_name = message.file.name or None
                    performer = message.file.performer or ''
                    fileTitle = message.file.title or ''
                    if performer is not None and fileTitle is not None:

                        fileTitle = performer + ' ' + fileTitle
                    text = message.text or ''
                    if text:
                        text = text.replace(
                            '#', '').replace('\n', '').replace('\\', '\\\\')
                    raw_text = message.raw_text or None
                    date = message.date or None
                    fileType = 'Photo'
                    fileDuration = message.file.duration
                    FileSize = message.file.size
                    if fileTitle is not None or fileTitle != ' ':
                        try:
                            fileTitle = fileTitle + \
                                '.' + file_name.split('.')[1]
                        except:
                            pass

                    pathName = uniqueId = uuid.uuid4().hex

                    try:
                        path = await message.download_media(file="downloads\\" + pathName)
                        pass
                    except:
                        down_is_success = 0
                        pass
                    if path:
                        # printed after download is done
                        print('File saved to', path)
                        down_is_success = 1

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
                    INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, FileSize, FileDuration, FileTitle, FileType,IsDownloaded, Group_Id, FilePath)
                    VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{},{},'{}');
                    '''.format(message_Id, text, file_name, text, raw_text, FileSize, fileDuration or 0, fileTitle,
                               fileType,
                               down_is_success,
                               group.Id,
                               path)

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
                        with open('Errors.txt', 'w', encoding='utf-8') as f:
                            f.write(insert)
                        pass
                    except Exception as e:
                        print(e)
                    pass
            pass

        pass

        # Music
        count = 0
        async for message in telethon_client_mbnz.iter_messages(group.address,
                                                                filter=InputMessagesFilterMusic,
                                                                reverse=True):
            # if flag == True:
            #     continue
            try:
                count += 1

                message_Id = message.id
                print(count)
                down_is_success = 0

                if message.media:
                    file_name = message.file.name or None
                    performer = message.file.performer or ''
                    fileTitle = message.file.title or ''
                    if performer is not None and fileTitle is not None:
                        fileTitle = performer + ' ' + fileTitle
                    text = message.text or ''
                    if text:
                        text = text.replace('\n', ' ').replace('\\', '\\\\')
                    raw_text = message.raw_text or None
                    date = message.date or None
                    fileType = 'Music'
                    fileDuration = message.file.duration
                    FileSize = message.file.size
                    if fileTitle is not None or fileTitle != ' ':
                        try:
                            fileTitle = fileTitle + \
                                '.' + file_name.split('.')[1]
                        except:
                            pass

                    pathName = uniqueId = uuid.uuid4().hex

                    try:
                        path = await message.download_media(file="downloads\\" + pathName)
                        # printed after download is done

                        pass
                    except:
                        path = 'none'
                        pass

                    if path:
                        print('File saved to', path)
                        down_is_success = 1
                    if path == 'none':
                        print('File saved to', path)
                        down_is_success = 0

            except errors.FloodWaitError as e:
                print('Have to sleep', e.seconds, 'seconds')
                time.sleep(e.seconds)
                print(message.raw_text)
                # await client.send_message("me", '#Check this \n' + message.raw_text)
                count = count + 1
                print('count is: ' + str(count))
                pass
            except Exception as e:
                print(e)

            finally:

                insert = '''
                            INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, FileSize, FileDuration, FileTitle, FileType,IsDownloaded, Group_Id,FilePath)
                            VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{},{},'{}');
                            '''.format(message_Id, text, file_name, text, raw_text, FileSize, fileDuration or 0,
                                       fileTitle,
                                       fileType,
                                       down_is_success,
                                       group.Id, path)

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
                        with open('Errors.txt', 'a', 'utf8') as f:
                            f.write(insert)
                        pass
                    except Exception as e:
                        print(e)
                    pass
            pass

        pass

        # Voices
        count = 0
        async for message in telethon_client_mbnz.iter_messages(group.address,
                                                                filter=InputMessagesFilterVoice,
                                                                reverse=True):
            # if flag == True:
            #     continue
            try:
                count += 1
                message_Id = message.id
                print(count)
                down_is_success = 0

                if message.media:
                    file_name = message.file.name or None
                    performer = message.file.performer or ''
                    fileTitle = message.file.title or ''
                    if performer is not None and fileTitle is not None:
                        fileTitle = performer + ' ' + fileTitle
                    text = message.text or ''
                    if text:
                        text = text.replace('\\', '\\\\').replace('\'', '\'\'')
                    raw_text = message.raw_text or None
                    date = message.date or None
                    fileType = 'Media'
                    fileDuration = message.file.duration
                    FileSize = message.file.size
                    if fileTitle is not None or fileTitle != ' ':
                        try:
                            fileTitle = fileTitle + \
                                '.' + file_name.split('.')[1]
                        except:
                            pass

                    pathName = uniqueId = uuid.uuid4().hex

                    try:
                        path = await message.download_media(file="downloads\\" + pathName)
                        pass
                    except:
                        path = 'none'
                        pass
                    # printed after download is done
                    if path:
                        print('File saved to', path)
                        down_is_success = 1
                    if path == 'none':
                        down_is_success = 0

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
                                            INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, FileSize, FileDuration, FileTitle, FileType,IsDownloaded, Group_Id,FilePath)
                                            VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{},{},'{}');
                                            '''.format(message_Id, text, file_name, text, raw_text, FileSize,
                                                       fileDuration or 0,
                                                       fileTitle,
                                                       fileType,
                                                       down_is_success,
                                                       group.Id, path)

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
                        with open('Errors.txt', 'a', 'utf8') as f:
                            f.write(insert)
                            f.write('\n')
                        pass
                    except Exception as e:
                        print(e)
                    pass
            pass

        pass

        # roundvoice
        count = 0
        async for message in telethon_client_mbnz.iter_messages(group.address,
                                                                filter=InputMessagesFilterRoundVoice,
                                                                reverse=True):

            # if flag == True:
            #     continue
            try:
                count += 1
                message_Id = message.id
                print(count)
                down_is_success = 0

                if message.media:
                    file_name = message.file.name or None
                    performer = message.file.performer or ''
                    fileTitle = message.file.title or ''
                    if performer is not None and fileTitle is not None:
                        fileTitle = performer + ' ' + fileTitle
                    text = message.text or ''
                    if text:
                        text = text.replace(
                            '#', '').replace('\n', '').replace('\\', '\\\\')
                    raw_text = message.raw_text or None
                    date = message.date or None
                    fileType = 'RoundVoice'
                    fileDuration = message.file.duration
                    FileSize = message.file.size
                    if fileTitle is not None or fileTitle != ' ':
                        try:
                            fileTitle = fileTitle + \
                                '.' + file_name.split('.')[1]
                        except:
                            pass

                    pathName = uniqueId = uuid.uuid4().hex

                    try:
                        path = await message.download_media(file="downloads\\" + pathName)
                        pass
                    except:
                        path = 'none'
                        pass
                    # printed after download is done
                    if path:
                        print('File saved to', path)
                        down_is_success = 1
                    if path == 'none':
                        down_is_success = 0

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
                                            INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, FileSize, FileDuration, FileTitle, FileType,IsDownloaded, Group_Id,FilePath)
                                            VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{},{},'{}');
                                            '''.format(message_Id, text, file_name, text, raw_text, FileSize,
                                                       fileDuration or 0,
                                                       fileTitle,
                                                       fileType,
                                                       down_is_success,
                                                       group.Id, path)

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
                        with open('Errors.txt', 'w', 'utf-8') as f:
                            f.write(insert)
                            f.write('\n')
                        pass
                    except Exception as e:
                        print(e)
                    pass
            pass

        pass

        # video
        count = 0
        async for message in telethon_client_mbnz.iter_messages(group.address,
                                                                filter=InputMessagesFilterVideo,
                                                                reverse=True):

            message_Id = message.id
            # if ( message_Id > 410):
            #         flag = False

            try:
                count += 1

                # if flag:
                #     continue
                print(count)
                down_is_success = 0

                if message.media:
                    file_name = message.file.name or None
                    performer = message.file.performer or ''
                    fileTitle = message.file.title or ''
                    if performer is not None and fileTitle is not None:
                        fileTitle = performer + ' ' + fileTitle
                    text = message.text or ''
                    if text:
                        text = text.replace(
                            '#', '').replace('\n', '').replace('\\', '\\\\')
                    raw_text = message.raw_text or None
                    date = message.date or None
                    fileType = 'Video'
                    fileDuration = message.file.duration
                    FileSize = message.file.size
                    if fileTitle is not None or fileTitle != ' ':
                        try:
                            fileTitle = fileTitle + \
                                '.' + file_name.split('.')[1]
                        except:
                            pass

                    pathName = uniqueId = uuid.uuid4().hex

                    try:
                        path = await message.download_media(file="downloads\\" + pathName)
                    except:
                        path = 'none'
                        pass
                    # printed after download is done
                    if path:
                        print('File saved to', path)
                        down_is_success = 1
                    if path == 'none':
                        down_is_success = 0

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

                try:
                    insert = '''
                                                INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, FileSize, FileDuration, FileTitle, FileType,IsDownloaded, Group_Id,FilePath)
                                                VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{},{},'{}');
                                                '''.format(message_Id, text, file_name, text, raw_text, FileSize,
                                                           fileDuration or 0,
                                                           fileTitle,
                                                           fileType,
                                                           down_is_success,
                                                           group.Id, path)

                    insert = insert.replace("'s ", "''s ").replace(
                        "\\", "\\\\")
                    conn = sqlite3.connect('PickupGroups.db')
                    cursor = conn.cursor()
                    cursor.execute(insert)
                    conn.commit()
                    pass

                except Exception as ex:

                    try:
                        with open('Errors.txt', 'w', encoding='utf-8') as f:
                            f.write(insert)
                            f.write(str(ex))
                            f.write('\n')
                        pass
                    except Exception as ex:
                        print(ex)
                    pass
            pass

        pass
        # roundVideo

        count = 0
        async for message in telethon_client_mbnz.iter_messages(group.address,
                                                                filter=InputMessagesFilterRoundVideo,
                                                                reverse=True):
            # if flag == True:
            #     continue
            try:
                count += 1
                message_Id = message.id
                print(count)
                down_is_success = 0

                if message.media:
                    file_name = message.file.name or None
                    performer = message.file.performer or ''
                    fileTitle = message.file.title or ''
                    if performer is not None and fileTitle is not None:
                        fileTitle = performer + ' ' + fileTitle
                    text = message.text or ''
                    if text:
                        text = text.replace(
                            '#', '').replace('\n', '').replace('\\', '\\\\')
                    raw_text = message.raw_text or None
                    date = message.date or None
                    fileType = 'RoundVideo'
                    fileDuration = message.file.duration
                    FileSize = message.file.size
                    if fileTitle is not None or fileTitle != ' ':
                        try:
                            fileTitle = fileTitle + \
                                '.' + file_name.split('.')[1]
                        except:
                            pass

                    pathName = uniqueId = uuid.uuid4().hex

                    try:

                        path = await message.download_media(file="downloads\\" + pathName)
                        pass
                    except:
                        path = 'none'
                        pass
                    # printed after download is done
                    if path:
                        print('File saved to', path)
                        down_is_success = 1
                    if path == 'none':
                        down_is_success = 0

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
                                            INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, FileSize, FileDuration, FileTitle, FileType,IsDownloaded, Group_Id,FilePath)
                                            VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{},{},'{}');
                                            '''.format(message_Id, text, file_name, text, raw_text, FileSize,
                                                       fileDuration or 0,
                                                       fileTitle,
                                                       fileType,
                                                       down_is_success,
                                                       group.Id, path)

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
                        with open('Errors.txt', 'w', encoding='utf-8') as f:
                            f.write(insert)
                        pass
                    except Exception as e:
                        print(e)
                    pass
            pass

        pass
        # document
        count = 0
        async for message in telethon_client_mbnz.iter_messages(group.address,
                                                                filter=InputMessagesFilterDocument,
                                                                reverse=True):

            message_Id = message.id
            # if (message_Id > 410):
            #     flag = False
            # if flag == True:
            #     continue
            try:
                count += 1

                print(count)
                down_is_success = 0

                if message.media:
                    file_name = message.file.name or None
                    performer = message.file.performer or ''
                    fileTitle = message.file.title or ''
                    if performer is not None and fileTitle is not None:
                        fileTitle = performer + ' ' + fileTitle
                    text = message.text or ''
                    if text:
                        text = text.replace(
                            '#', '').replace('\n', ' ').replace('\\', '\\\\')
                    raw_text = message.raw_text or None
                    date = message.date or None
                    fileType = 'Document'
                    fileDuration = message.file.duration
                    FileSize = message.file.size
                    if fileTitle is not None or fileTitle != ' ':
                        try:
                            fileTitle = fileTitle + \
                                '.' + file_name.split('.')[1]
                        except:
                            pass

                    pathName = uniqueId = uuid.uuid4().hex

                    try:
                        print('downloading')
                        path = await message.download_media(file="downloads\\" + pathName)
                        pass
                    except:
                        path = 'none'
                        pass
                    # printed after download is done
                    if path == 'none':
                        down_is_success = 0
                    if path:
                        print('File saved to', path)
                        down_is_success = 1

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

                try:
                    insert = '''
                                                INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, FileSize, FileDuration, FileTitle, FileType,IsDownloaded, Group_Id,FilePath)
                                                VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{},{},'{}');
                                                '''.format(message_Id, text, file_name, text, raw_text, FileSize,
                                                           fileDuration or 0,
                                                           fileTitle,
                                                           fileType,
                                                           down_is_success,
                                                           group.Id, path)

                    insert = insert.replace("'s ", "''s ").replace(
                        "\\", "\\\\")
                    conn = sqlite3.connect('PickupGroups.db')
                    cursor = conn.cursor()
                    cursor.execute(insert)
                    conn.commit()
                    pass

                except Exception as e:
                    print(e)

                    try:
                        with open('Errors.txt', 'w', encoding='utf-8') as f:
                            f.write(insert)
                        pass
                    except Exception as e:
                        print(e)
                    pass
            pass

        pass

    pass

    pass


with telethon_client_mbnz:
    telethon_client_mbnz.loop.run_until_complete(Main())

print('finished')

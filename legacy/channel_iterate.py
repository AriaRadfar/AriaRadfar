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


class ChannelIterate:
    mbnz_api_id = 11850432
    mbnz_api_hash = "2c38966be914ff7f108b63bafca0a038"
    telethon_client_mbnz = TelegramClient('mbnz', mbnz_api_id, mbnz_api_hash)

    Message_ID = ""
    Text = ""
    FileName = ""
    Caption = ""
    RawText = ""
    Date = ""
    FileSize = ""
    FileDuration = ""
    FileTitle = ""
    file_type = ""

    destination_group = ""

    @staticmethod
    async def parseMessages(message, type, count=0):
        try:
            Message_ID = message.id
            down_is_success = 0

            if message.media:
                file_name = message.file.name or None
                performer = message.file.performer or None
                file_title = performer + ' ' + message.file.title
                text = message.text or None
                if text:
                    text = text.replace(
                        '#', '').replace('\n', '').replace('\\', '\\\\')
                raw_text = message.raw_text or None
                date = message.date or None
                file_type = type
                file_duration = message.file.duration
                file_size = message.file.size
                if file_title:
                    file_title = file_title + \
                        '.' + file_name.split('.')[1]

                path_name = file_title or file_name or str(Message_ID) or text

                try:
                    success = await message.download_media(
                        file=str(count) + "-" + path_name)
                    if success:
                        down_is_success = 1
                    # path = await message.download_media(file="F:\\\Pico Man\\pics\\temp\\" + str(count)+"-" + path_name)
                    pass
                except:
                    path = await message.download_media(
                        file=str(count) + "-" + str(Message_ID))
                    if path:
                        down_is_success = 1
                # print('File saved to', path)  # printed after download is done

        except errors.FloodWaitError as e:
            print('Have to sleep', e.seconds, 'seconds')
            time.sleep(e.seconds)
            print(message.raw_text)
            # await client.send_message(DorehayeAliTxtGroup, '#تکست ایز هیر \n' + message.raw_text)
            count = count + 1
            print('count is: ' + str(count))
            pass

        finally:

            insert = '''
            INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, file_size, FileDuration, FileTitle, FileType,down_is_success, Group_Id)
            VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{},{});
            '''.format(Message_ID, text, file_name, text, raw_text, file_size, file_duration or 0, file_title,
                       file_type,
                       down_is_success, PickupGroups.GroupId)
            try:
                conn = sqlite3.connect('PickupGroups.db')
                cursor = conn.cursor()
                cursor.execute(insert)
                conn.commit()
                pass

            except:
                with(type + '.txt', 'a', 'utf-8') as f:
                    f.write(insert)
                pass

        pass

    @staticmethod
    async def IterateMessages(PickupGroups, telethon_client1=telethon_client_mbnz,
                              telethon_client2=telethon_client_mbnz, destinationGroup=destination_group):

        count = 0
        telethon_client1.start()
        async for message in telethon_client1.iter_messages(
                PickupGroups.address,
                filter=InputMessagesFilterMusic,
                reverse=False):
            ChannelIterate.parseMessages(message, type='Music')

        pass

    @staticmethod
    async def IteratePhotos(PickupGroups, telethon_client1=telethon_client_mbnz, telethon_client2=telethon_client_mbnz,
                            destinationGroup=destination_group):
        count = 0
        async for message in telethon_client1.iter_messages(PickupGroups.address,
                                                            filter=InputMessagesFilterPhotos,
                                                            reverse=False):

            await ChannelIterate.parseMessages(message, type='Photo')

            try:
                Message_ID = message.id
                down_is_success = 0

                if message.media:
                    file_name = message.file.name or None
                    performer = message.file.performer or None
                    fileTitle = performer + ' ' + message.file.title
                    text = message.text or None
                    if text:
                        text = text.replace(
                            '#', '').replace('\n', '').replace('\\', '\\\\')
                    raw_text = message.raw_text or None
                    date = message.date or None
                    fileType = 'Audio'
                    fileDuration = message.file.duration
                    FileSize = message.file.size
                    if fileTitle:
                        fileTitle = fileTitle + \
                            '.' + file_name.split('.')[1]

                    pathName = fileTitle or file_name or str(
                        Message_ID) or text

                    try:
                        # path = await message.download_media(file="F:\\\Pico Man\\pics\\temp\\" + str(count)+"-" + pathName)
                        pass
                    except:
                        path = await message.download_media(
                            file="F:\\pics\\temp\\" + str(count) + "-" + str(Message_ID))
                    # print('File saved to', path)  # printed after download is done

            except errors.FloodWaitError as e:
                print('Have to sleep', e.seconds, 'seconds')
                time.sleep(e.seconds)
                print(message.raw_text)
                # await client.send_message(DorehayeAliTxtGroup, '#تکست ایز هیر \n' + message.raw_text)
                count = count + 1
                print('count is: ' + str(count))
                pass

            finally:

                insert = '''
                INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, FileSize, FileDuration, FileTitle, FileType, Group_Id)
                VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{});
                '''.format(Message_ID, text, file_name, text, raw_text, FileSize, fileDuration or 0, fileTitle, fileType,
                           PickupGroups.GroupId)
                try:
                    conn = sqlite3.connect('PickupGroups.db')
                    cursor = conn.cursor()
                    cursor.execute(insert)
                    conn.commit()
                    pass

                except:
                    with('messages.txt', 'a', 'utf-8') as f:
                        f.write(insert)
                    pass
            pass

        pass

    @staticmethod
    async def IterateMusic(PickupGroups, telethon_client1=telethon_client_mbnz, telethon_client2=telethon_client_mbnz,
                           destinationGroup=destination_group):
        count = 0
        async for message in telethon_client1.iter_messages(PickupGroups.address,
                                                            filter=InputMessagesFilterMusic,
                                                            reverse=False):
            try:
                Message_ID = message.id
                down_is_success = 0

                if message.media:
                    fileName = message.file.name or None
                    performer = message.file.performer or None
                    fileTitle = performer + ' ' + message.file.title
                    text = message.text or None
                    if text:
                        text = text.replace(
                            '#', '').replace('\n', '').replace('\\', '\\\\')
                    raw_text = message.raw_text or None
                    date = message.date or None
                    fileType = 'Audio'
                    fileDuration = message.file.duration
                    FileSize = message.file.size
                    if fileTitle:
                        fileTitle = fileTitle + \
                            '.' + fileName.split('.')[1]

                    pathName = fileTitle or fileName or str(Message_ID) or text

                    try:
                        # path = await message.download_media(file="F:\\\Pico Man\\pics\\temp\\" + str(count)+"-" + pathName)
                        pass
                    except:
                        path = await message.download_media(
                            file="F:\\pics\\temp\\" + str(count) + "-" + str(Message_ID))
                    # print('File saved to', path)  # printed after download is done

            except errors.FloodWaitError as e:
                print('Have to sleep', e.seconds, 'seconds')
                time.sleep(e.seconds)
                print(message.raw_text)
                # await client.send_message(DorehayeAliTxtGroup, '#تکست ایز هیر \n' + message.raw_text)
                count = count + 1
                print('count is: ' + str(count))
                pass

            finally:

                insert = '''
                INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, FileSize, FileDuration, FileTitle, FileType, Group_Id)
                VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{});
                '''.format(Message_ID, text, fileName, text, raw_text, FileSize, fileDuration or 0, fileTitle, fileType,
                           PickupGroups.GroupId)
                try:
                    conn = sqlite3.connect('PickupGroups.db')
                    cursor = conn.cursor()
                    cursor.execute(insert)
                    conn.commit()
                    pass

                except:
                    with('messages.txt', 'a', 'utf-8') as f:
                        f.write(insert)
                    pass
            pass

        pass

    @staticmethod
    async def IterateVoice(PickupGroups, telethon_client1=telethon_client_mbnz, telethon_client2=telethon_client_mbnz,
                           destinationGroup=destination_group):
        count = 0
        async for message in telethon_client1.iter_messages(PickupGroups.address, filter=InputMessagesFilterVoice,
                                                            reverse=False):
            try:
                Message_ID = message.id
                down_is_success = 0

                if message.media:
                    fileName = message.file.name or None
                    performer = message.file.performer or None
                    fileTitle = performer + ' ' + message.file.title
                    text = message.text or None
                    if text:
                        text = text.replace(
                            '#', '').replace('\n', '').replace('\\', '\\\\')
                    raw_text = message.raw_text or None
                    date = message.date or None
                    fileType = 'Audio'
                    fileDuration = message.file.duration
                    FileSize = message.file.size
                    if fileTitle:
                        fileTitle = fileTitle + \
                            '.' + fileName.split('.')[1]

                    pathName = fileTitle or fileName or str(Message_ID) or text

                    try:
                        # path = await message.download_media(file="F:\\\Pico Man\\pics\\temp\\" + str(count)+"-" + pathName)
                        pass
                    except:
                        path = await message.download_media(
                            file="F:\\pics\\temp\\" + str(count) + "-" + str(Message_ID))
                    # print('File saved to', path)  # printed after download is done

            except errors.FloodWaitError as e:
                print('Have to sleep', e.seconds, 'seconds')
                time.sleep(e.seconds)
                print(message.raw_text)
                # await client.send_message(DorehayeAliTxtGroup, '#تکست ایز هیر \n' + message.raw_text)
                count = count + 1
                print('count is: ' + str(count))
                pass

            finally:

                insert = '''
                INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, FileSize, FileDuration, FileTitle, FileType, Group_Id)
                VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{});
                '''.format(Message_ID, text, fileName, text, raw_text, FileSize, fileDuration or 0, fileTitle, fileType,
                           PickupGroups.GroupId)
                try:
                    conn = sqlite3.connect('PickupGroups.db')
                    cursor = conn.cursor()
                    cursor.execute(insert)
                    conn.commit()
                    pass

                except:
                    with('messages.txt', 'a', 'utf-8') as f:
                        f.write(insert)
                    pass
            pass

        pass

    @staticmethod
    async def IterateVideo(telethon_client1=telethon_client_mbnz,
                           telethon_client2=telethon_client_mbnz,
                           destinationGroup=destination_group):

        count = 0
        async for message in telethon_client1.iter_messages(PickupGroups.address, filter=InputMessagesFilterVideo,
                                                            reverse=False):
            try:
                Message_ID = message.id
                down_is_success = 0

                if message.media:
                    fileName = message.file.name or None
                    performer = message.file.performer or None
                    fileTitle = performer + ' ' + message.file.title
                    text = message.text or None
                    if text:
                        text = text.replace(
                            '#', '').replace('\n', '').replace('\\', '\\\\')
                    raw_text = message.raw_text or None
                    date = message.date or None
                    fileType = 'Audio'
                    fileDuration = message.file.duration
                    FileSize = message.file.size
                    if fileTitle:
                        fileTitle = fileTitle + \
                            '.' + fileName.split('.')[1]

                    pathName = fileTitle or fileName or str(Message_ID) or text

                    try:
                        # path = await message.download_media(file="F:\\\Pico Man\\pics\\temp\\" + str(count)+"-" + pathName)
                        pass
                    except:
                        path = await message.download_media(
                            file="F:\\pics\\temp\\" + str(count) + "-" + str(Message_ID))
                    # print('File saved to', path)  # printed after download is done

            except errors.FloodWaitError as e:
                print('Have to sleep', e.seconds, 'seconds')
                time.sleep(e.seconds)
                print(message.raw_text)
                # await client.send_message(DorehayeAliTxtGroup, '#تکست ایز هیر \n' + message.raw_text)
                count = count + 1
                print('count is: ' + str(count))
                pass

            finally:

                insert = '''
                INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, FileSize, FileDuration, FileTitle, FileType, Group_Id)
                VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{});
                '''.format(Message_ID, text, fileName, text, raw_text, FileSize, fileDuration or 0, fileTitle, fileType,
                           PickupGroups.GroupId)
                try:
                    conn = sqlite3.connect('PickupGroups.db')
                    cursor = conn.cursor()
                    cursor.execute(insert)
                    conn.commit()
                    pass

                except:
                    with('messages.txt', 'a', 'utf-8') as f:
                        f.write(insert)
                    pass
            pass

        pass

    @staticmethod  # check the document check what the document is ? are long video files also documents
    async def IterateDocuments(PickupGroups, telethon_client1=telethon_client_mbnz,
                               telethon_client2=telethon_client_mbnz, destinationGroup=destination_group):
        count = 0
        async for message in telethon_client1.iter_messages(PickupGroups.address, filter=InputMessagesFilterDocument,
                                                            reverse=False):
            try:
                Message_ID = message.id
                down_is_success = 0

                if message.media:
                    fileName = message.file.name or None
                    performer = message.file.performer or None
                    fileTitle = performer + ' ' + message.file.title
                    text = message.text or None
                    if text:
                        text = text.replace(
                            '#', '').replace('\n', '').replace('\\', '\\\\')
                    raw_text = message.raw_text or None
                    date = message.date or None
                    fileType = 'Audio'
                    fileDuration = message.file.duration
                    FileSize = message.file.size
                    if fileTitle:
                        fileTitle = fileTitle + \
                            '.' + fileName.split('.')[1]

                    pathName = fileTitle or fileName or str(Message_ID) or text

                    try:
                        # path = await message.download_media(file="F:\\\Pico Man\\pics\\temp\\" + str(count)+"-" + pathName)
                        pass
                    except:
                        path = await message.download_media(
                            file="F:\\pics\\temp\\" + str(count) + "-" + str(Message_ID))
                    # print('File saved to', path)  # printed after download is done

            except errors.FloodWaitError as e:
                print('Have to sleep', e.seconds, 'seconds')
                time.sleep(e.seconds)
                print(message.raw_text)
                # await client.send_message(DorehayeAliTxtGroup, '#تکست ایز هیر \n' + message.raw_text)
                count = count + 1
                print('count is: ' + str(count))
                pass

            finally:

                insert = '''
                INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, FileSize, FileDuration, FileTitle, FileType, Group_Id)
                VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{});
                '''.format(Message_ID, text, fileName, text, raw_text, FileSize, fileDuration or 0, fileTitle, fileType,
                           PickupGroups.GroupId)
                try:
                    conn = sqlite3.connect('PickupGroups.db')
                    cursor = conn.cursor()
                    cursor.execute(insert)
                    conn.commit()
                    pass

                except:
                    with('messages.txt', 'a', 'utf-8') as f:
                        f.write(insert)
                    pass
            pass

        pass
        pass

    @staticmethod
    async def IterateFiles(PickupGroups, telethon_client1=telethon_client_mbnz, telethon_client2=telethon_client_mbnz,
                           destinationGroup=destination_group):
        count = 0
        async for message in telethon_client1.iter_messages(PickupGroups.address, filter=InputMessagesFilterDocument,
                                                            reverse=False):
            try:
                Message_ID = message.id
                down_is_success = 0

                if message.media:
                    file_name = message.file.name or None
                    performer = message.file.performer or None
                    file_title = performer + ' ' + message.file.title
                    text = message.text or None
                    if text:
                        text = text.replace(
                            '#', '').replace('\n', '').replace('\\', '\\\\')
                    raw_text = message.raw_text or None
                    date = message.date or None
                    fileType = 'Audio'
                    fileDuration = message.file.duration
                    fileSize = message.file.size
                    if file_title:
                        file_title = file_title + \
                            '.' + file_name.split('.')[1]

                    pathName = file_title or file_name or str(
                        Message_ID) or text

                    try:
                        # path = await message.download_media(file="F:\\\Pico Man\\pics\\temp\\" + str(count)+"-" + pathName)
                        pass
                    except:
                        path = await message.download_media(
                            file="F:\\pics\\temp\\" + str(count) + "-" + str(Message_ID))
                    # print('File saved to', path)  # printed after download is done

            except errors.FloodWaitError as e:
                print('Have to sleep', e.seconds, 'seconds')
                time.sleep(e.seconds)
                print(message.raw_text)
                # await client.send_message(DorehayeAliTxtGroup, '#تکست ایز هیر \n' + message.raw_text)
                count = count + 1
                print('count is: ' + str(count))
                pass

            finally:

                insert = '''
                INSERT INTO Messages (Message_Id,FileText, FileName, Caption, RawText, fileSize, FileDuration, FileTitle, FileType, Group_Id)
                VALUES ({},'{}','{}','{}','{}',{},{},'{}','{}',{});
                '''.format(Message_ID, text, file_name, text, raw_text, fileSize, fileDuration or 0, file_title, fileType,
                           PickupGroups.GroupId)
                try:
                    conn = sqlite3.connect('PickupGroups.db')
                    cursor = conn.cursor()
                    cursor.execute(insert)
                    conn.commit()
                    pass

                except:
                    with('messages.txt', 'a', 'utf-8') as f:
                        f.write(insert)
                    pass
            pass

        pass
        pass

    # @staticmethod
    # async def IterateFiles(PickupGroups, telethon_client=telethon_client, destinationGroup=destination_group):
    #     count = 0
    #     async for message in telethon_client.iter_messages(PickupGroups.address, filter=InputMessagesFilterMusic,
    #                                                        reverse=False):
    #         # print('dd-11')
    #         pass

    #     pass

    # @staticmethod
    # async def IterateFiles(PickupGroups, telethon_client=telethon_client, destinationGroup=destination_group):
    #     count = 0
    #     async for message in telethon_client.iter_messages(PickupGroups.address, filter=InputMessagesFilterMusic,
    #                                                        reverse=False):
    #         # print('dd-11')
    #         pass

    #     pass

    # @staticmethod
    # async def IterateFiles(PickupGroups, telethon_client=telethon_client, destinationGroup=destination_group):
    #     count = 0
    #     async for message in telethon_client.iter_messages(PickupGroups.address, filter=InputMessagesFilterMusic,
    #                                                        reverse=False):
    #         # print('dd-11')
    #         pass

    #     pass

    # @staticmethod
    # async def IterateFiles(PickupGroups, telethon_client=telethon_client, destinationGroup=destination_group):
    #     count = 0
    #     async for message in telethon_client.iter_messages(PickupGroups.address, filter=InputMessagesFilterMusic,
    #                                                        reverse=False):
    #         # print('dd-11')
    #         pass

    #     pass

    # @staticmethod
    # async def IterateFiles(PickupGroups, telethon_client=telethon_client, destinationGroup=destination_group):
    #     count = 0
    #     async for message in telethon_client.iter_messages(PickupGroups.address, filter=InputMessagesFilterMusic,
    #                                                        reverse=False):
    #         # print('dd-11')
    #         pass

    # @staticmethod
    # async def IterateFiles(PickupGroups, telethon_client=telethon_client, destinationGroup=destination_group):
    #     count = 0
    #     async for message in telethon_client.iter_messages(PickupGroups.address, filter=InputMessagesFilterMusic,
    #                                                        reverse=False):
    #         # print('dd-11')
    #         pass

    #     pass


pass

# InputMessagesFilterMusic
# InputMessagesFilterUrl
# InputMessagesFilterDocument


# async def main():
#     count = 0
#     async for message in client.iter_messages('https://t.me/+kmiX6B10lYcxY2Q0', filter=InputMessagesFilterMusic, reverse=False):
#         try:
#             Message_ID = message.id

#             if message.media:
#                 FileName = message.file.name or None
#                 performer = message.file.performer or None
#                 FileTitle = performer + ' ' + message.file.title

#                 text = message.text or None
#                 if text:
#                     text = text.replace(
#                         '#', '').replace('\n', '').replace('\\', '\\\\')
#                 Raw_text = message.raw_text or None
#                 date = message.date or None
#                 FileType = 'Audio'
#                 FileSize = message.file.size
#                 if FileTitle:
#                     FileTitle = FileTitle + \
#                         '.'+FileName.split('.')[1]

#                 pathName = FileTitle or FileName or str(Message_ID) or text

#                 try:
#                     # path = await message.download_media(file="F:\\\Pico Man\\pics\\temp\\" + str(count)+"-" + pathName)
#                     pass
#                 except:
#                     path = await message.download_media(file="F:\\\Pico Man\\pics\\temp\\" + str(count)+"-" + str(Message_ID))
#                 # print('File saved to', path)  # printed after download is done

#         except errors.FloodWaitError as e:
#             print('Have to sleep', e.seconds, 'seconds')
#             time.sleep(e.seconds)
#             print(message.raw_text)
#             # await client.send_message(DorehayeAliTxtGroup, '#دوره_های_عالی \n' + message.raw_text)
#             count = count + 1
#             print('count is: '+str(count))
#             pass
#         finally:
#             #         insert = '''
#             #             insert into  DoreHayeAli(
#             #                 Message_ID
#             #  ,FileText
#             #  ,FileName
#             #  ,Caption
#             #  ,RawText

#             #  ,FileSize
#             #  ,FileDuration
#             #  ,FileTitle
#             #  ,FileType
#             #  ,FilePath)
#             #  values({},N'{}',N'{}',N'{}',N'{}',{},{},N'{}','{}')

#             #         '''.format(Message_ID, text, FileName, text, Raw_text, FileSize, FileDuration or 0, FileTitle, FileType, path)
#             #         print(insert)
#             #         try:
#             #             # cursor.execute(insert)
#             #             # cursor.commit()
#             #             pass
#             #         except Exception as f:
#             #             print(f)
#             #             continue
#             #             pass

#             pass


def test():

    pass
# with client:
#     client.loop.run_until_complete(main())
# os.system("shutdown /h")  # hibernate


#     /****** Script for SelectTopNRows command from SSMS  ******/
# SELECT TOP (1000)  Id
#       , Message_ID
#       , Text
#       , FileName
#       , Caption
#       , RawText
#       , Date
#       , FileSize
#       , FileDuration
#       , FileTitle
#       , FileType
#   FROM  Telegram . dbo . DoreHayeAli


#   insert = '''
#             insert into  Messages(
#                 Message_Id
#  ,FileText
#  ,FileName
#  ,Caption
#  ,RawText

#  ,FileSize
#  ,FileDuration
#  ,FileTitle
#  ,FileType
#  ,FilePath)
#  values({},N'{}',N'{}',N'{}',N'{}',{},{},N'{}','{}')

#         '''.format(Message_ID, text, FileName, text, Raw_text, FileSize, FileDuration or 0, FileTitle, FileType, path)
#         print(insert)
#         try:
#             # cursor.execute(insert)
#             # cursor.commit()
#             pass
#         except Exception as f:
#             print(f)
#             continue
#             pass


# client.send_file(chat, '/my/photos/me.jpg', caption="It's me!")

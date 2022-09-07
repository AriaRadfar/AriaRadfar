import asyncio
from fileinput import filename
from pyexpat.errors import messages
from telethon import TelegramClient, sync
import time
from telethon import errors
import os
from telethon.tl.types import *
import pyodbc


api_id = 11850432
api_hash = "2c38966be914ff7f108b63bafca0a038"
DorehayeAliTxtGroup = 'fso_dpd_nkwoddhgs'


connection_string = ("Driver={SQL Server Native Client 11.0};"
                     "Server=DESKTOP-AHLCUSV\DEVELOP;"
                     "Database=Telegram;"
                     "Trusted_Connection=yes;")
conn = pyodbc.connect(connection_string)


cursor = conn.cursor()

Message_ID = ""
Text = ""
FileName = ""
Caption = ""
RawText = ""
Date = ""
FileSize = ""
FileDuration = ""
FileTitle = ""
FileType = ""

client = TelegramClient('anon', api_id, api_hash)

# InputMessagesFilterMusic
# InputMessagesFilterUrl
# InputMessagesFilterDocument


async def main():
    count = 0
    async for message in client.iter_messages('me', filter=InputMessagesFilterMusic, reverse=False):
        try:
            count = count + 1
            # if count < 400:
            #     continue
            Message_ID = message.id

            if message.media:
                FileName = message.file.name or None
                FileTitle = message.file.title or None

                text = message.text or ''
                if text:
                    text = text
                    # .replace(
                    #     '#', '').replace('\n', '')
                Raw_text = message.raw_text or ''
                date = message.date or None
                FileType = 'photo'
                FileSize = message.file.size
                pathName = FileName or FileTitle or text or str(Message_ID)

                try:
                    path = await message.download_media(file="F:\\\Pico Man\\pics\\temp\\")
                except:
                    path = await message.download_media(file="F:\\\Pico Man\\pics\\temp\\")
                print('File saved to', path)  # printed after download is done
                try:

                    sent = await client.send_file(DorehayeAliTxtGroup, path,
                                                  caption='#Audio ' + str(count) + '\n' +
                                                  + FileName+'\n' + Raw_text)
                    if sent:
                        os.remove(path)
                    time.sleep(0.3)
                    pass
                except errors.MediaCaptionTooLongError:
                    # sent = await client.send_file(DorehayeAliTxtGroup, path,
                    #                               caption='#photo ' + str(count))
                    pass
                except:
                    continue

        except errors.FloodWaitError as e:
            print('Have to sleep', e.seconds, 'seconds')
            time.sleep(e.seconds)
            print(message.raw_text)
            if path:
                sent = await client.send_file(DorehayeAliTxtGroup, path,
                                              caption='#photo ' + str(count) + '\n'+Raw_text)
            if sent:
                if os.path.exists(path):
                    os.remove(path)

            print('count is: '+str(count))
            pass


with client:
    client.loop.run_until_complete(main())


# /****** Script for SelectTopNRows command from SSMS  ******/
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


async def main():
    count = 0
    async for message in client.iter_messages('me', reverse=True):

        # print(type(message.date))
        # print(message.date)
        # # print(message.id, message.text)
        print('message Id is: ' + str(message.id))

        if not message.media:
            try:
                print(message.raw_text)
                await client.send_message(DorehayeAliTxtGroup, '#دوره_های_عالی \n' + message.raw_text)
                count = count + 1
                print('count is: '+str(count))
                continue
                pass
            except errors.FloodWaitError as e:

                print('Have to sleep', e.seconds, 'seconds')
                time.sleep(e.seconds)
                print(message.raw_text)
                await client.send_message(DorehayeAliTxtGroup, '#دوره_های_عالی \n' + message.raw_text)
                count = count + 1
                print('count is: '+str(count))
                continue

            except:
                with open('last telegram post.txt', 'a', encoding='utf8') as f:
                    f.write('\n')
                    f.write('id:')
                    f.write(str(message.id) or None)
                    f.write('\n')
                    f.write('text-start:')
                    f.write('\n')
                    f.write('text:  '+str(message.raw_text) or None)
                    f.write('text-End')
                    f.write('\n')

                continue
            pass

            # await client.send_message('me', message.raw_text)

            # You can download media from messages, too!
            # The method will return the path where the file was saved.
        # if message.media:
        #     # if message.caption is not None:
        #     #     print('message caption is: ' + str(message.caption))
        #     print(message.file.name or 'no name')
        #     # print(message.file.caption)
        #     print(message.file.size)
        #     print(message.file.title)
        #     print(message.file.duration)

        #     path = await message.download_media(file="Telethon//"+str(message.id))
        #     print('File saved to', path)  # printed after download is done
        # if message.text:
        #     print(message.text)


with client:
    client.loop.run_until_complete(main())
    print(count)
    client.send_message(DorehayeAliTxtGroup, str(count))
    os.system("shutdown /h")

from os import curdir
import sqlite3
from enum import Enum


class PickupGroups:
    Id = 0

    def __init__(self, Id, PersianName, EnglishName, address):
        self.Id = Id
        self.name = PersianName
        self.englishName = EnglishName
        self.address = address
        PickupGroups.Id += 1

    pass


class Db:
    def __init__(self):
        conn = sqlite3.connect('PickupGroups.db')
        cursor = conn.cursor()

        GroupsCreation = '''
        CREATE TABLE IF NOT EXISTS Groups(
           Group_Id INTEGER PRIMARY KEY AUTOINCREMENT,
           EnglishName           TEXT       NULL,
           Addreess            INT        NULL,
           PersianName        Text        Null,
           IsFinished          INT        NULL
        );
        '''
        floodtable = '''
        CREATE TABLE IF NOT EXISTS Flood(
           Id INTEGER PRIMARY KEY AUTOINCREMENT,
           MessageId           Int       NULL,
           GroupId            INT        NULL
           
        );
        '''

        mainDatabaseCreation = '''
        CREATE TABLE IF NOT EXISTS Messages(
           Id INTEGER PRIMARY KEY AUTOINCREMENT,
           Message_Id        INT        NOT NULL,
           FileText          TEXT       NULL,
           FileName          INT        NULL,
           Caption           Text       Null,
           RawText           Text       Null,
           FileSize          INT        NULL ,
           FileDuration      INT        NULL   ,
           FileTitle         TEXT       NULL ,
           FileType          TEXT       NULL ,
           FilePath          TEXT       NULL ,
            IsDownloaded     INT        NULL ,
           IsUploaded       INT        NULL,
           count            INT        Null,
           destinationMessageId Int    Null,

           Group_Id Int not null,

           FOREIGN KEY (Group_Id)
            REFERENCES Groups (Group_Id)
            ON UPDATE CASCADE
            ON DELETE CASCADE

        );
        '''
        mainDatabaseCreation2 = '''
                CREATE TABLE IF NOT EXISTS Messages2(
                   Id INTEGER PRIMARY KEY AUTOINCREMENT,
                   Message_Id        INT        NOT NULL,
                   FileText          TEXT       NULL,
                   FileName          INT        NULL,
                   Caption           Text       Null,
                   RawText           Text       Null,
                   FileSize          INT        NULL ,
                   FileDuration      INT        NULL   ,
                   FileTitle         TEXT       NULL ,
                   FileType          TEXT       NULL ,
                   FilePath          TEXT       NULL ,
                    IsDownloaded     INT        NULL ,
                   IsUploaded       INT        NULL,
                   count            INT        Null,
                   destinationMessageId Int    Null,

                   Group_Id Int not null,
                   Done Int not null default 0 ,

                   FOREIGN KEY (Group_Id)
                    REFERENCES Groups (Group_Id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE

                );
                '''

        cursor.execute(GroupsCreation)
        # commit the changes to db
        conn.commit()

        cursor.execute(floodtable)
        # commit the changes to db
        conn.commit()

        cursor.execute(mainDatabaseCreation2)
        conn.commit()

        cursor.execute(mainDatabaseCreation)
        conn.commit()

        # close the connection
        conn.close()

        pass

    @staticmethod
    def selectAllGroups():
        groups = []
        conn = sqlite3.connect('PickupGroups.db')
        cursor = conn.cursor()
        cursor.execute('select * from Groups')
        rows = cursor.fetchall()
        for row in rows:
            Id = row[0]
            english_name = row[1]
            address = row[2]
            isFinished = row[4]
            if isFinished != 0:
                continue
            if address is None or address == 'None' or address == 'none':
                continue
            persian_name = row[3]
            # print(row)
            groups.append(PickupGroups(Id=Id, EnglishName=english_name,
                          address=address, PersianName=persian_name))
            pass

        return groups

    @staticmethod
    def checkItemExists(message_id, group_id):
        conn = sqlite3.connect('PickupGroups.db')
        cursor = conn.cursor()
        cursor.execute(
            f'select * from Messages where Message_Id = {message_id} and Group_Id = {group_id} and IsDownloaded = 1 and IsUploaded = 1')
        rows = cursor.fetchall()
        for row in rows:
            is_uploaded = row[12]
            destinationId = row[14]
            # TODO: CHECK THESE RETURN VALUES FROM TABEL AND CHANGE DESTINATIONMESSAGEID
            # CHECK IF IS DOWNLOADED and UPLOADED
            if is_uploaded == 1 and row[15] is not None:
                return True, destinationId or 0
        return False, 0
        pass

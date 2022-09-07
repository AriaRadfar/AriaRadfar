import sqlite3


conn = sqlite3.connect("databases\\forward.db")
cursor = conn.cursor()

conn2 = sqlite3.connect("databases\\forward2.db")
cursor2 = conn.cursor()

query = '''
    create table if not exists Tbl_Forwards(
        Id integer primary key autoincrement,
        ChannelAddress Text Null,
        ChannelName Text Null,
        ChannelAgent Integer Null,
        LastMessageId Integer null,
        Done integer null,
        MyOrder integer null
    );
'''
cursor2.execute(query)
conn2.commit()


def readChannels(path):
    channels = []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            line = line.replace("#", "")
            if line == "":
                continue
            channels.append(line)

    return channels


def addToDb(channel):
    cursor.execute(f'''
    SELECT Id, ChannelAddress, LastMessageId, ChannelName, ChannelAgent, Done
        FROM Tbl_Forwards
        where ChannelAddress is '{channel}';''')
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(
            f"INSERT INTO tbl_forwards( ChannelAddress, Done) VALUES ('{channel}',0)")
        conn.commit()


chanlls = readChannels(r'logs\group_list_agent2.txt')
for el in chanlls:
    addToDb(el)


def copy():
    cursor.execute('''
    SELECT Id, ChannelAddress, LastMessageId, ChannelName, ChannelAgent, Done, column_definition, MyOrder
        FROM Tbl_Forwards;
    ''')
    
    pass    

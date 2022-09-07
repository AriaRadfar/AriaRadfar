import sqlite3


conn = sqlite3.connect('PickupGroups.db')
cursor = conn.cursor()


# PersianName = ''
# # EnglishName = input('Write the English Name: ')

# while True:
#     PersianName = input('Persian Name: ')
#     if PersianName == 'end':
#         break
#     query = '''
# insert into Groups(PersianName)
# values('{}')
# '''.format(PersianName)

#     cursor.execute(query)
#     # EnglishName = input('English Name: ')
#     conn.commit()

#     pass


query = 'select * from Groups'
cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row[3])
    EnglishName = input("English Name: ")
    query = '''
        update Groups
        set EnglishName = '{}'
        where PersianName = '{}'
        '''.format(EnglishName, row[3])
    cursor.execute(
        query
    )
    conn.commit()
    pass

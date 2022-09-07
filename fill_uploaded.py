import sqlite3


main_conn = sqlite3.connect('Upload.db')
main_cursor = main_conn.cursor()


message_conn = sqlite3.connect('PickupGroups.db')
message_cursor = message_conn.cursor()

main_cursor.execute('select * from UploadedMessages')
rows = main_cursor.fetchall()


for row in rows:
    Id = row[0]
    file_path = row[3]
    message_id = row[1]
    q = f'update Messages set IsUploaded =1 where Id ={Id}'
    message_cursor.execute(q)
    message_conn.commit()

print('finish')

import database

conn = database.connection()
cursor = conn.cursor()
cursor.execute('DELETE FROM "points";')
cursor.execute('DELETE FROM "songs";')
conn.commit()
conn.close()
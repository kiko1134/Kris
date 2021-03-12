import sqlite3

DB_NAME = 'chat_app.db'

conn = sqlite3.connect(DB_NAME)



conn.cursor().execute('''
    CREATE TABLE IF NOT EXISTS Users
    (
        users_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT NOT NULL UNIQUE ,
        password TEXT NOT NULL
    )
''')
conn.commit()


conn.cursor().execute('''
    CREATE TABLE IF NOT EXISTS Friendships
    (
        friendship_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_name TEXT,
        friend_name TEXT,
        nickname_1 TEXT,
        nickname_2 TEXT
    )
''')
conn.commit()


conn.cursor().execute('''
    CREATE TABLE IF NOT EXISTS Messages
    (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        friendship_id INTEGER,
        sent_by_id TEXT,
        content TEXT
    )
''')
conn.commit()



class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()

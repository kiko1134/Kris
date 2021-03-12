import hashlib
from database import DB


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


    def create(self):
        with DB() as db:
            values = (self.username, self.password)
            db.execute('''
                INSERT INTO Users (name, password)
                VALUES (?, ?)''', values)
            return self

    @staticmethod
    def find_by_username(username):
        if not username:
            return None
        with DB() as db:
            row = db.execute(
                'SELECT * FROM Users WHERE name = ?',
                (username,)
            ).fetchone()
            if row:
                return User(*row)

    @staticmethod
    def get_usernames():
        with DB() as db:
            rows = db.execute('SELECT name FROM Users').fetchall()
            if rows:
                names = []
                for row in rows:
                    names.append(row[0])
                return names


    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def verify_password(self, password):
        return self.password == password

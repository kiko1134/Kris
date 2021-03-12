from database import DB

class Friendship:
    def __init__(self, friendship_id, sender_name, friend_name, nickname_1, nickname_2):
        self.friendship_id = friendship_id
        self.sender_name = sender_name
        self.friend_name = friend_name
        self.nickname_1 = nickname_1
        self.nickname_2 = nickname_2

    @staticmethod
    def all_for_u(sender_name):
        with DB() as db:
            rows = db.execute('SELECT * FROM Friendships WHERE sender_name = ? OR friend_name = ?', (sender_name, sender_name)).fetchall()
            return [Friendship(*row) for row in rows]

    @staticmethod
    def find(friendship_id):
        with DB() as db:
            row = db.execute('SELECT * FROM Friendships WHERE friendship_id = ?', (friendship_id,)).fetchone()
            if row is None:
                return
            return Friendship(*row)

    def find_by_name(friend_name):
        with DB() as db:
            row = db.execute('SELECT * FROM Friendships WHERE friend_name = ?', (friend_name,)).fetchone()
            return Friendship(*row)

    def create(self):
        with DB() as db:
            values = (self.sender_name, self.friend_name, self.nickname_1, self.nickname_2)
            db.execute('''
                INSERT INTO Friendships (sender_name, friend_name, nickname_1, nickname_2)
                VALUES (?, ?, ?, ?)''', values)
            return self

    def save(self):
        with DB() as db:
            values =  (self.sender_name, self.friend_name, self.nickname_1, self.nickname_2, self.friendship_id)
            db.execute('UPDATE Friendships SET sender_name = ?, friend_name = ?, nickname_1 = ?, nickname_2 = ? WHERE friendship_id = ?', values)
            return self

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM Friendships WHERE friendship_id = ?', (self.friendship_id,))

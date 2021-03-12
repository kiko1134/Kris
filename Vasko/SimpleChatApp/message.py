from database import DB

class Message:
    def __init__(self, message_id, friendship_id, sent_by_id, content):
        self.message_id = message_id
        self.friendship_id = friendship_id
        self.sent_by_id = sent_by_id
        self.content = content

    @staticmethod
    def all_with(friendship_id):
        with DB() as db:
            rows = db.execute('SELECT * FROM Messages WHERE friendship_id = ?', (friendship_id,)).fetchall()
            return [Message(*row) for row in rows]


    def create(self):
        with DB() as db:
            values = (self.friendship_id, self.sent_by_id, self.content)
            row = db.execute('INSERT INTO Messages(friendship_id, sent_by_id, content) VALUES (?, ?, ?)', values)
            return self

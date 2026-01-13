import sqlite3
from datetime import datetime

class MockDB:
    def init_app(self, app):
        pass
    
    def create_all(self):
        pass

class MockSerializerMixin:
    def to_dict(self):
        result = {}
        for key in ['id', 'body', 'username', 'created_at', 'updated_at']:
            if hasattr(self, key):
                value = getattr(self, key)
                if isinstance(value, datetime):
                    result[key] = value.isoformat()
                else:
                    result[key] = value
        return result

class Message(MockSerializerMixin):
    def __init__(self, body=None, username=None, id=None):
        self.id = id
        self.body = body
        self.username = username
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def query(cls):
        return MockQuery()

class MockQuery:
    def filter_by(self, **kwargs):
        return self
    
    def filter(self, *args):
        return self
    
    def first(self):
        conn = sqlite3.connect('app.db')
        conn.row_factory = sqlite3.Row
        result = conn.execute('SELECT * FROM messages LIMIT 1').fetchone()
        conn.close()
        if result:
            msg = Message()
            for key in result.keys():
                setattr(msg, key, result[key])
            return msg
        return None
    
    def all(self):
        conn = sqlite3.connect('app.db')
        conn.row_factory = sqlite3.Row
        results = conn.execute('SELECT * FROM messages ORDER BY created_at ASC').fetchall()
        conn.close()
        messages = []
        for result in results:
            msg = Message()
            for key in result.keys():
                setattr(msg, key, result[key])
            messages.append(msg)
        return messages

db = MockDB()
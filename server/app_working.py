from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        conn = get_db_connection()
        messages = conn.execute(
            'SELECT * FROM messages ORDER BY created_at ASC'
        ).fetchall()
        conn.close()
        
        return jsonify([dict(message) for message in messages])
    
    elif request.method == 'POST':
        data = request.get_json()
        body = data['body']
        username = data['username']
        created_at = datetime.utcnow().isoformat()
        updated_at = created_at
        
        conn = get_db_connection()
        cursor = conn.execute(
            'INSERT INTO messages (body, username, created_at, updated_at) VALUES (?, ?, ?, ?)',
            (body, username, created_at, updated_at)
        )
        message_id = cursor.lastrowid
        conn.commit()
        
        # Get the created message
        new_message = conn.execute(
            'SELECT * FROM messages WHERE id = ?', (message_id,)
        ).fetchone()
        conn.close()
        
        return jsonify(dict(new_message)), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    conn = get_db_connection()
    
    if request.method == 'PATCH':
        data = request.get_json()
        body = data['body']
        updated_at = datetime.utcnow().isoformat()
        
        conn.execute(
            'UPDATE messages SET body = ?, updated_at = ? WHERE id = ?',
            (body, updated_at, id)
        )
        conn.commit()
        
        # Get the updated message
        updated_message = conn.execute(
            'SELECT * FROM messages WHERE id = ?', (id,)
        ).fetchone()
        conn.close()
        
        if updated_message is None:
            return jsonify({'error': 'Message not found'}), 404
            
        return jsonify(dict(updated_message))
    
    elif request.method == 'DELETE':
        conn.execute('DELETE FROM messages WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return '', 204

if __name__ == '__main__':
    app.run(port=5555, debug=True)
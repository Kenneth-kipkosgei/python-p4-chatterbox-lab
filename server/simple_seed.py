#!/usr/bin/env python3

import sqlite3
from datetime import datetime
from random import choice

# Sample data
usernames = ["Alice", "Bob", "Charlie", "Diana", "Duane"]
messages = [
    "Hello everyone!",
    "How's everyone doing today?",
    "Great weather we're having!",
    "Anyone up for a chat?",
    "Hope you're all having a wonderful day!",
    "What's new with everyone?",
    "Beautiful morning, isn't it?",
    "Looking forward to the weekend!",
    "Anyone have exciting plans?",
    "Just wanted to say hi!"
]

# Connect to database
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Clear existing messages
cursor.execute("DELETE FROM messages")

# Insert sample messages
for i in range(10):
    body = choice(messages)
    username = choice(usernames)
    created_at = datetime.utcnow().isoformat()
    updated_at = created_at
    
    cursor.execute(
        "INSERT INTO messages (body, username, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (body, username, created_at, updated_at)
    )

conn.commit()
conn.close()

print("Database seeded successfully!")
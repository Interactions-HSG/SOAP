import sqlite3
import json
import os
import datetime

class PollDatabase:
    def __init__(self, db_path=None):
        """Initialize the poll database connection"""
        if db_path is None:
            # Use the default location in the database directory
            dir_path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(os.path.dirname(dir_path), 'polls_database.db')
        
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables()
        
    def connect(self):
        """Connect to the SQLite database"""
        self.connection = sqlite3.connect(self.db_path)
        # Enable foreign keys
        self.connection.execute("PRAGMA foreign_keys = ON")
        # Return rows as dictionaries
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        # Create users table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            first_seen TIMESTAMP NOT NULL,
            last_seen TIMESTAMP NOT NULL
        )
        ''')
        
        # Create poll_responses table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS poll_responses (
            response_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            poll_id TEXT NOT NULL,
            page TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        ''')
        
        self.connection.commit()
    
    def add_or_update_user(self, user_id):
        """Add a new user or update last_seen time for existing user"""
        now = datetime.datetime.now().isoformat()
        
        # Check if user exists
        self.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if self.cursor.fetchone():
            # Update last_seen time
            self.cursor.execute(
                "UPDATE users SET last_seen = ? WHERE user_id = ?", 
                (now, user_id)
            )
        else:
            # Create new user
            self.cursor.execute(
                "INSERT INTO users (user_id, first_seen, last_seen) VALUES (?, ?, ?)",
                (user_id, now, now)
            )
        
        self.connection.commit()
        return user_id
    
    def save_response(self, user_id, poll_id, page, response_data):
        """Save a poll response for a specific user"""
        # Ensure user exists
        self.add_or_update_user(user_id)
        
        # Convert response_data to JSON string if it's not already a string
        if not isinstance(response_data, str):
            response_data = json.dumps(response_data)
        
        now = datetime.datetime.now().isoformat()
        
        # Check if response already exists for this user and poll_id
        self.cursor.execute(
            "SELECT response_id FROM poll_responses WHERE user_id = ? AND poll_id = ?",
            (user_id, poll_id)
        )
        existing = self.cursor.fetchone()
        
        if existing:
            # Update existing response
            self.cursor.execute(
                "UPDATE poll_responses SET response = ?, timestamp = ? WHERE response_id = ?",
                (response_data, now, existing['response_id'])
            )
        else:
            # Create new response
            self.cursor.execute(
                "INSERT INTO poll_responses (user_id, poll_id, page, response, timestamp) VALUES (?, ?, ?, ?, ?)",
                (user_id, poll_id, page, response_data, now)
            )
        
        self.connection.commit()
        return True
    
    def get_user_responses(self, user_id):
        """Get all poll responses for a specific user"""
        self.cursor.execute(
            "SELECT * FROM poll_responses WHERE user_id = ? ORDER BY timestamp",
            (user_id,)
        )
        
        # Convert rows to dictionaries and parse response JSON
        results = []
        for row in self.cursor.fetchall():
            row_dict = dict(row)
            # Parse the response JSON if it's valid JSON
            try:
                row_dict['response'] = json.loads(row_dict['response'])
            except json.JSONDecodeError:
                pass  # Keep as string if it's not JSON
            results.append(row_dict)
        
        return results
    
    def get_all_responses_for_poll(self, poll_id):
        """Get all responses for a specific poll across all users"""
        self.cursor.execute(
            "SELECT * FROM poll_responses WHERE poll_id = ? ORDER BY timestamp",
            (poll_id,)
        )
        
        # Convert rows to dictionaries and parse response JSON
        results = []
        for row in self.cursor.fetchall():
            row_dict = dict(row)
            # Parse the response JSON if it's valid JSON
            try:
                row_dict['response'] = json.loads(row_dict['response'])
            except json.JSONDecodeError:
                pass  # Keep as string if it's not JSON
            results.append(row_dict)
        
        return results
    
    def get_poll_statistics(self, poll_id):
        """Get statistics for a specific poll"""
        responses = self.get_all_responses_for_poll(poll_id)
        
        # Count unique users
        unique_users = set(r['user_id'] for r in responses)
        
        # Try to calculate average response if responses are numeric
        try:
            avg_response = sum(float(r['response']) for r in responses) / len(responses) if responses else 0
        except (ValueError, TypeError):
            avg_response = None
        
        return {
            'poll_id': poll_id,
            'total_responses': len(responses),
            'unique_users': len(unique_users),
            'average_response': avg_response
        }
    
    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
    
    def __del__(self):
        """Destructor to ensure database connection is closed"""
        self.close()
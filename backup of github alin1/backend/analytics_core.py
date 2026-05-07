import sqlite3
from datetime import datetime
from pathlib import Path

# Set up the database file path next to your vector DBs
CURRENT_DIR = Path(__file__).parent.absolute()
DB_PATH = CURRENT_DIR / "subject_dbs" / "student_analytics.db"

def init_analytics_db():
    """Creates the analytics database and tables if they don't exist."""
    # Ensure the directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Table to track every interaction
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            subject TEXT,
            is_faq BOOLEAN,
            user_query TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("📊 Analytics Database initialized successfully.")

def log_interaction(subject: str, is_faq: bool, user_query: str):
    """Silently logs a student's query to the database."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO interactions (timestamp, subject, is_faq, user_query)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, subject, is_faq, user_query))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Analytics Logging Error: {e}")

# Run initialization when the file is imported
init_analytics_db()
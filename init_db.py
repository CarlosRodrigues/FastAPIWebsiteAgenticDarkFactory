import sqlite3
import os

DB_DIR = ".commonai"
DB_PATH = os.path.join(DB_DIR, "ontology.db")

def init_database():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    print("🛠️ Initializing Ontology Database...")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'in_progress', 'completed'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            action TEXT NOT NULL,
            value TEXT NOT NULL,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'in_progress', 'completed')),
            FOREIGN KEY (feature_id) REFERENCES features (id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS acceptance_criteria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_story_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            passed BOOLEAN DEFAULT 0,
            FOREIGN KEY (user_story_id) REFERENCES user_stories (id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ac_id INTEGER NOT NULL,
            test_type TEXT NOT NULL CHECK(test_type IN ('unit', 'integration', 'ui', 'security')),
            output TEXT,
            passed BOOLEAN DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ac_id) REFERENCES acceptance_criteria (id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_story_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            retries INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_story_id) REFERENCES user_stories (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print(f"🎉 Database initialized successfully at {DB_PATH}")

if __name__ == "__main__":
    init_database()
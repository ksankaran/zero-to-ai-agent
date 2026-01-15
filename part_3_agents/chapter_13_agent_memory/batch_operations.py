# From: AI Agents Book - Chapter 13, Section 13.7
# File: batch_operations.py

import sqlite3
from datetime import datetime, timedelta


class BatchMemoryProcessor:
    """Process multiple conversations efficiently with batch operations.
    
    Note: This assumes a message_store table with columns:
    - session_id, message_type, content, timestamp
    
    See retention_policy.py or production_memory_manager.py for
    the table creation schema.
    """
    
    def __init__(self, db_path):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database with required schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS message_store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                message_type TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_session_id 
            ON message_store(session_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON message_store(timestamp)
        """)
        
        conn.commit()
        conn.close()
    
    def add_message(self, session_id: str, message_type: str, content: str, 
                    timestamp: datetime = None):
        """Add a message (for testing purposes)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO message_store (session_id, message_type, content, timestamp)
            VALUES (?, ?, ?, ?)
        """, (session_id, message_type, content, timestamp or datetime.now()))
        
        conn.commit()
        conn.close()
    
    def batch_cleanup(self, session_ids, cutoff_date):
        """Delete old messages for multiple users in one query."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Use IN clause for batch operation
        placeholders = ','.join('?' * len(session_ids))
        cursor.execute(f"""
            DELETE FROM message_store 
            WHERE session_id IN ({placeholders})
            AND timestamp < ?
        """, (*session_ids, cutoff_date))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted
    
    def batch_export(self, session_ids):
        """Export data for multiple users efficiently."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        placeholders = ','.join('?' * len(session_ids))
        cursor.execute(f"""
            SELECT session_id, message_type, content, timestamp 
            FROM message_store 
            WHERE session_id IN ({placeholders})
            ORDER BY session_id, timestamp
        """, session_ids)
        
        results = cursor.fetchall()
        conn.close()
        
        # Group by session_id
        exports = {}
        for session_id, msg_type, content, timestamp in results:
            if session_id not in exports:
                exports[session_id] = []
            exports[session_id].append({
                "type": msg_type,
                "content": content,
                "timestamp": str(timestamp)
            })
        
        return exports
    
    def batch_delete_users(self, session_ids):
        """Delete all data for multiple users (GDPR bulk request)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        placeholders = ','.join('?' * len(session_ids))
        cursor.execute(f"""
            DELETE FROM message_store 
            WHERE session_id IN ({placeholders})
        """, session_ids)
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted
    
    def get_stats(self):
        """Get database statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM message_store")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT session_id) FROM message_store")
        sessions = cursor.fetchone()[0]
        
        conn.close()
        return {"total_messages": total, "total_sessions": sessions}


# Usage
if __name__ == "__main__":
    import os
    
    # Use a fresh test database
    test_db = "batch_test.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    processor = BatchMemoryProcessor(test_db)
    
    # Add sample data - some old, some new
    old_date = datetime.now() - timedelta(days=60)
    recent_date = datetime.now() - timedelta(days=5)
    
    print("Adding sample messages...")
    
    # Old messages (will be cleaned up)
    processor.add_message("user_1", "human", "Old message 1", old_date)
    processor.add_message("user_1", "ai", "Old response 1", old_date)
    processor.add_message("user_2", "human", "Old message 2", old_date)
    
    # Recent messages (will be kept)
    processor.add_message("user_1", "human", "Recent message", recent_date)
    processor.add_message("user_2", "human", "Recent message", recent_date)
    processor.add_message("user_3", "human", "User 3 message", recent_date)
    
    print(f"Stats before cleanup: {processor.get_stats()}")
    
    # Batch cleanup for multiple users (messages older than 30 days)
    users_to_clean = ["user_1", "user_2", "user_3"]
    cutoff = datetime.now() - timedelta(days=30)
    
    deleted = processor.batch_cleanup(users_to_clean, cutoff)
    print(f"\nBatch cleanup: deleted {deleted} old messages")
    print(f"Stats after cleanup: {processor.get_stats()}")
    
    # Batch export
    print("\nBatch export:")
    exports = processor.batch_export(["user_1", "user_2"])
    for user_id, messages in exports.items():
        print(f"  {user_id}: {len(messages)} messages")
    
    # Batch delete (GDPR)
    deleted = processor.batch_delete_users(["user_3"])
    print(f"\nBatch delete user_3: {deleted} messages deleted")
    print(f"Final stats: {processor.get_stats()}")
    
    # Cleanup test file
    os.remove(test_db)
    print("\nTest complete!")
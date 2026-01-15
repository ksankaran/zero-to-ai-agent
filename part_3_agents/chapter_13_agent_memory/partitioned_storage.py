# From: AI Agents Book - Chapter 13, Section 13.7
# File: partitioned_storage.py

from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
from langchain_community.chat_message_histories import SQLChatMessageHistory


class PartitionedStorage:
    """Partition conversation data by date for large-scale applications."""
    
    def __init__(self, base_path="chat_history"):
        self.base_path = base_path
    
    def get_db_path(self, date=None):
        """Get database path for specific date partition."""
        if date is None:
            date = datetime.now()
        
        year_month = date.strftime("%Y_%m")
        return f"{self.base_path}_{year_month}.db"
    
    def get_session_history(self, session_id, date=None):
        """Get history from appropriate partition."""
        db_path = self.get_db_path(date)
        return SQLChatMessageHistory(
            session_id=session_id,
            connection=f"sqlite:///{db_path}"
        )
    
    def list_partitions(self):
        """List all existing partitions."""
        import glob
        return glob.glob(f"{self.base_path}_*.db")


# Usage
if __name__ == "__main__":
    storage = PartitionedStorage()
    
    # Current month
    current_history = storage.get_session_history("user_123")
    print(f"Current DB: {storage.get_db_path()}")
    
    # Specific month (for historical queries)
    jan_2024 = datetime(2024, 1, 1)
    old_db = storage.get_db_path(date=jan_2024)
    print(f"January 2024 DB: {old_db}")
    
    # List all partitions
    print(f"Existing partitions: {storage.list_partitions()}")

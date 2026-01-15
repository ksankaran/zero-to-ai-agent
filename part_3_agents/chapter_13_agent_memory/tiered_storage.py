# From: AI Agents Book - Chapter 13, Section 13.7
# File: tiered_storage.py

from datetime import datetime


class TieredStorage:
    """Move old conversations to cheaper storage tiers.
    
    Tiers:
    - Hot (< 7 days): Fast access, e.g., Redis
    - Warm (7-30 days): Moderate speed, e.g., SQLite
    - Cold (> 30 days): Slow but cheap, e.g., S3
    """
    
    def __init__(self):
        self.hot_storage = {}   # Recent - in-memory or Redis
        self.warm_storage = {}  # 7-30 days - SQLite
        self.cold_storage = {}  # 30+ days - S3 or similar
    
    def get_tier(self, message_date):
        """Determine storage tier based on message age."""
        age_days = (datetime.now() - message_date).days
        
        if age_days < 7:
            return "hot"
        elif age_days < 30:
            return "warm"
        else:
            return "cold"
    
    def store_message(self, session_id, message, timestamp=None):
        """Store message in appropriate tier."""
        if timestamp is None:
            timestamp = datetime.now()
        
        tier = self.get_tier(timestamp)
        
        if tier == "hot":
            self._store_hot(session_id, message, timestamp)
        elif tier == "warm":
            self._store_warm(session_id, message, timestamp)
        else:
            self._store_cold(session_id, message, timestamp)
    
    def get_messages(self, session_id, message_date=None):
        """Route to appropriate storage tier."""
        if message_date is None:
            # Get from all tiers
            messages = []
            messages.extend(self._get_from_hot(session_id))
            messages.extend(self._get_from_warm(session_id))
            messages.extend(self._get_from_cold(session_id))
            return messages
        
        tier = self.get_tier(message_date)
        
        if tier == "hot":
            return self._get_from_hot(session_id)
        elif tier == "warm":
            return self._get_from_warm(session_id)
        else:
            return self._get_from_cold(session_id)
    
    def migrate_to_colder_tier(self):
        """Move aged data to appropriate tier (run periodically)."""
        moved = {"hot_to_warm": 0, "warm_to_cold": 0}
        
        # Move from hot to warm
        for session_id, messages in list(self.hot_storage.items()):
            for msg in messages[:]:
                if self.get_tier(msg["timestamp"]) == "warm":
                    self._store_warm(session_id, msg["content"], msg["timestamp"])
                    messages.remove(msg)
                    moved["hot_to_warm"] += 1
        
        # Move from warm to cold
        for session_id, messages in list(self.warm_storage.items()):
            for msg in messages[:]:
                if self.get_tier(msg["timestamp"]) == "cold":
                    self._store_cold(session_id, msg["content"], msg["timestamp"])
                    messages.remove(msg)
                    moved["warm_to_cold"] += 1
        
        return moved
    
    # Tier-specific implementations
    def _store_hot(self, session_id, message, timestamp):
        if session_id not in self.hot_storage:
            self.hot_storage[session_id] = []
        self.hot_storage[session_id].append({"content": message, "timestamp": timestamp})
    
    def _store_warm(self, session_id, message, timestamp):
        if session_id not in self.warm_storage:
            self.warm_storage[session_id] = []
        self.warm_storage[session_id].append({"content": message, "timestamp": timestamp})
    
    def _store_cold(self, session_id, message, timestamp):
        if session_id not in self.cold_storage:
            self.cold_storage[session_id] = []
        self.cold_storage[session_id].append({"content": message, "timestamp": timestamp})
    
    def _get_from_hot(self, session_id):
        return self.hot_storage.get(session_id, [])
    
    def _get_from_warm(self, session_id):
        return self.warm_storage.get(session_id, [])
    
    def _get_from_cold(self, session_id):
        return self.cold_storage.get(session_id, [])


# Usage
if __name__ == "__main__":
    storage = TieredStorage()
    
    # Store recent message (goes to hot)
    storage.store_message("user_123", "Hello!")
    
    # Store older message (simulated)
    from datetime import timedelta
    old_date = datetime.now() - timedelta(days=15)
    storage.store_message("user_123", "Old message", old_date)
    
    very_old_date = datetime.now() - timedelta(days=45)
    storage.store_message("user_123", "Very old message", very_old_date)
    
    print(f"Hot storage: {len(storage.hot_storage.get('user_123', []))} messages")
    print(f"Warm storage: {len(storage.warm_storage.get('user_123', []))} messages")
    print(f"Cold storage: {len(storage.cold_storage.get('user_123', []))} messages")

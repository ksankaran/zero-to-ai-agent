# Save as: data_retention.py
"""
Data retention and privacy management for AI agents.
Handles conversation storage, cleanup, and GDPR compliance.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class ConversationManager:
    """
    Manage conversation data with retention policies.
    
    Implements:
    - Automatic cleanup of old conversations
    - User data deletion (GDPR compliance)
    - Safe data storage
    """
    
    def __init__(
        self,
        retention_days: int = 30,
        storage_dir: str = "conversations"
    ):
        self.retention_days = retention_days
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        # In-memory storage for demo (use database in production)
        self.conversations: Dict[str, Dict[str, Any]] = {}
    
    def store_conversation(
        self,
        conversation_id: str,
        user_id: str,
        messages: List[Dict[str, str]]
    ) -> None:
        """
        Store a conversation with metadata.
        
        Messages are stored with user_id for later deletion if requested.
        """
        self.conversations[conversation_id] = {
            "user_id": user_id,
            "messages": messages,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        
        # Also persist to disk (for demo)
        self._save_to_disk(conversation_id)
        
        logger.info(f"Stored conversation {conversation_id[:8]}... for user {user_id}")
    
    def get_conversation(self, conversation_id: str) -> Dict[str, Any] | None:
        """Retrieve a conversation by ID."""
        return self.conversations.get(conversation_id)
    
    async def cleanup_old_conversations(self) -> int:
        """
        Delete conversations older than retention period.
        
        Run this on a schedule (e.g., daily cron job).
        Returns number of deleted conversations.
        """
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        deleted_count = 0
        
        to_delete = []
        for conv_id, data in self.conversations.items():
            created = datetime.fromisoformat(data["created_at"])
            if created < cutoff:
                to_delete.append(conv_id)
        
        for conv_id in to_delete:
            del self.conversations[conv_id]
            self._delete_from_disk(conv_id)
            deleted_count += 1
        
        logger.info(f"Cleaned up {deleted_count} old conversations (retention: {self.retention_days} days)")
        return deleted_count
    
    async def delete_user_data(self, user_id: str) -> int:
        """
        Delete ALL data for a user (GDPR compliance).
        
        This is a legal requirement - users can request deletion of their data.
        Returns number of deleted conversations.
        """
        to_delete = [
            conv_id for conv_id, data in self.conversations.items()
            if data["user_id"] == user_id
        ]
        
        for conv_id in to_delete:
            del self.conversations[conv_id]
            self._delete_from_disk(conv_id)
        
        logger.info(f"Deleted all data for user {user_id}: {len(to_delete)} conversations")
        return len(to_delete)
    
    def export_user_data(self, user_id: str) -> Dict[str, Any]:
        """
        Export all data for a user (GDPR data portability).
        
        Users have the right to request a copy of their data.
        """
        user_conversations = {
            conv_id: data
            for conv_id, data in self.conversations.items()
            if data["user_id"] == user_id
        }
        
        export = {
            "user_id": user_id,
            "export_date": datetime.now().isoformat(),
            "conversation_count": len(user_conversations),
            "conversations": user_conversations,
        }
        
        logger.info(f"Exported data for user {user_id}: {len(user_conversations)} conversations")
        return export
    
    def _save_to_disk(self, conversation_id: str) -> None:
        """Persist conversation to disk."""
        filepath = self.storage_dir / f"{conversation_id}.json"
        with open(filepath, 'w') as f:
            json.dump(self.conversations[conversation_id], f)
    
    def _delete_from_disk(self, conversation_id: str) -> None:
        """Delete conversation file from disk."""
        filepath = self.storage_dir / f"{conversation_id}.json"
        if filepath.exists():
            filepath.unlink()


# Database security reminders:
#
# ✅ Use parameterized queries (if using SQL):
#    cursor.execute(
#        "SELECT * FROM conversations WHERE id = %s", 
#        (conversation_id,)  # Parameter, not string formatting
#    )
#
# ❌ NEVER do this - SQL injection vulnerability:
#    cursor.execute(
#        f"SELECT * FROM conversations WHERE id = '{conversation_id}'"
#    )


if __name__ == "__main__":
    import asyncio
    
    # Demo
    print("Data Retention Manager Demo")
    print("=" * 50)
    
    manager = ConversationManager(retention_days=30)
    
    # Store some conversations
    manager.store_conversation(
        "conv-001",
        "user-alice",
        [
            {"role": "user", "content": "Hello!"},
            {"role": "assistant", "content": "Hi there!"}
        ]
    )
    
    manager.store_conversation(
        "conv-002",
        "user-alice",
        [
            {"role": "user", "content": "What's the weather?"},
            {"role": "assistant", "content": "I don't have weather data."}
        ]
    )
    
    manager.store_conversation(
        "conv-003",
        "user-bob",
        [
            {"role": "user", "content": "Help me with code"},
            {"role": "assistant", "content": "Sure, what do you need?"}
        ]
    )
    
    print(f"\nStored {len(manager.conversations)} conversations")
    
    # Export user data (GDPR)
    export = manager.export_user_data("user-alice")
    print(f"\nExported data for user-alice: {export['conversation_count']} conversations")
    
    # Delete user data (GDPR)
    async def demo_delete():
        deleted = await manager.delete_user_data("user-alice")
        print(f"\nDeleted {deleted} conversations for user-alice")
        print(f"Remaining conversations: {len(manager.conversations)}")
    
    asyncio.run(demo_delete())

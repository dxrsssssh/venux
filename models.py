# models.py - Using plain Python dicts/classes for structure, not Beanie Documents

from typing import Optional, List
from datetime import datetime

# No more `from beanie import Document, Indexed` here.
# These are now just structural guides or can be removed if not strictly needed for type hinting.

# --- Guild Configuration Structure Guide (Optional, can be dicts) ---
class GuildConfigData:
    def __init__(self, guild_id: int, prefix: str = "!", log_channel_id: Optional[int] = None, welcome_channel_id: Optional[int] = None):
        self.guild_id = guild_id
        self.prefix = prefix
        self.log_channel_id = log_channel_id
        self.welcome_channel_id = welcome_channel_id

    def to_dict(self):
        return {
            "guild_id": self.guild_id,
            "prefix": self.prefix,
            "log_channel_id": self.log_channel_id,
            "welcome_channel_id": self.welcome_channel_id,
        }

# --- User Profile / Leveling Structure Guide ---
class UserProfileData:
    def __init__(self, user_id: int, guild_id: int, xp: int = 0, level: int = 0, last_message_time: datetime = datetime.utcnow()):
        self.user_id = user_id
        self.guild_id = guild_id
        self.xp = xp
        self.level = level
        self.last_message_time = last_message_time
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "guild_id": self.guild_id,
            "xp": self.xp,
            "level": self.level,
            "last_message_time": self.last_message_time,
        }
# ... and so on for ReminderData, ModCaseData, CustomCommandData

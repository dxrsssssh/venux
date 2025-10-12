# models.py
from typing import Optional, List
from beanie import Document, Indexed
from datetime import datetime

# --- Guild Configuration Model ---
class GuildConfig(Document):
    guild_id: Indexed(int, unique=True)
    prefix: str = "!" # Default prefix
    log_channel_id: Optional[int] = None # Channel for moderation logs
    welcome_channel_id: Optional[int] = None # Channel for welcome messages
    
    class Settings:
        name = "guild_configs" # MongoDB collection name

# --- User Profile / Leveling Model ---
class UserProfile(Document):
    user_id: Indexed(int)
    guild_id: Indexed(int) # This makes levels per-guild
    xp: int = 0
    level: int = 0
    last_message_time: datetime = datetime.utcnow() # To prevent XP spam
    
    class Settings:
        name = "user_profiles"
        # Compound index for efficient per-guild user profile lookups
        unique_together = [("user_id", "guild_id")] 

# --- Reminder Model ---
class Reminder(Document):
    user_id: int
    channel_id: int # Channel where reminder was set (and should be sent)
    message_content: str
    remind_time: datetime # When the reminder should be sent
    created_at: datetime = datetime.utcnow()
    
    class Settings:
        name = "reminders"

# --- Moderation Case Model (Example) ---
class ModCase(Document):
    guild_id: int
    case_id: Indexed(int) # Auto-incrementing or unique ID for each case
    mod_id: int # Moderator who performed the action
    target_id: int # User affected by the action
    action: str # e.g., "kick", "ban", "mute", "warn"
    reason: str
    timestamp: datetime = datetime.utcnow()
    duration: Optional[int] = None # For mutes/bans with duration
    active: bool = True # For mutes/bans that can expire or be un-done

    class Settings:
        name = "mod_cases"
        unique_together = [("guild_id", "case_id")] # Ensure case IDs are unique per guild

# --- Custom Command Model ---
class CustomCommand(Document):
    guild_id: int
    command_name: Indexed(str)
    response: str
    created_by: int
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "custom_commands"
        unique_together = [("guild_id", "command_name")]

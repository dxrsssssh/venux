# cogs/moderation.py
import discord
from discord.ext import commands
from discord import app_commands
from utils import send_success_embed, send_error_embed, send_info_embed, send_warning_embed
from config import EMOJIS
from models import ModCase # Import your ModCase model

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        # Optional: A global check for all commands in this cog
        # e.g., ensure commands are not used in DMs unless specifically allowed
        if not ctx.guild:
            await send_error_embed(ctx, "DM Not Allowed", "This command can only be used in a server.")
            return False
        return True

    @commands.hybrid_command(
        name="kick",
        description="Kicks a member from the server."
    )
    @commands.has_permissions(kick_members=True) # Prefix command permission check
    @app_commands.default_permissions(kick_members=True) # Slash command permission check
    @app_commands.describe(
        member="The member to kick.",
        reason="The reason for kicking."
    )
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str = "No reason provided."):
        if member == ctx.author:
            return await send_error_embed(ctx, "Self-Kick Attempt", "You cannot kick yourself!")
        if member == self.bot.user: # Use self.bot.user instead of ctx.bot.user
            return await send_error_embed(ctx, "Bot-Kick Attempt", "I cannot kick myself!")
        if ctx.author.top_role <= member.top_role and ctx.author.id != self.bot.owner_id:
            return await send_error_embed(ctx, "Permission Denied", f"You cannot kick `{member.display_name}` as their highest role is equal to or higher than yours.")

        try:
            await member.kick(reason=reason)

            # Record in database
            latest_case = await ModCase.find_one(
                ModCase.guild_id == ctx.guild.id, 
                sort=[("case_id", -1)] # Get the highest case ID
            )
            case_id = (latest_case.case_id + 1) if latest_case else 1

            mod_case = ModCase(
                guild_id=ctx.guild.id,
                case_id=case_id,
                mod_id=ctx.author.id,
                target_id=member.id,
                action="kick",
                reason=reason,
                active=False # Kick is a one-time action
            )
            await mod_case.insert()

            await send_success_embed(
                ctx,
                "Member Kicked",
                f"{EMOJIS.get('moderation', '')} Successfully kicked `{member.display_name}` (`{member.id}`).\n**Reason:** {reason}\n**Case ID:** #{case_id}"
            )
            # You would also send this to a moderation log channel if configured in GuildConfig
        except discord.Forbidden:
            await send_error_embed(ctx, "Permission Error", "I don't have permission to kick this member. Make sure my role is higher than theirs and I have the `Kick Members` permission.")
        except Exception as e:
            await send_error_embed(ctx, "Kick Failed", f"An unexpected error occurred: `{e}`")

    # Add other moderation commands (ban, mute, warn, unban, etc.) following this pattern
    # Remember to create a "mute" role and manage it in your mute/unmute commands.
    # For mutes/tempbans, you'll need to run background tasks to check expiration times from the DB.

async def setup(bot):
    await bot.add_cog(Moderation(bot))

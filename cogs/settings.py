# cogs/settings.py
import discord
from discord.ext import commands
from discord import app_commands
from utils import send_success_embed, send_error_embed, send_info_embed
# from models import GuildConfig # <-- REMOVE THIS, or import GuildConfigData if using for structure

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db # Get the database object from the bot instance

    @commands.hybrid_command(
        name="setprefix",
        description="Sets a custom prefix for this server."
    )
    @commands.has_permissions(manage_guild=True)
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.describe(new_prefix="The new prefix for the bot.")
    async def setprefix(self, ctx: commands.Context, new_prefix: str):
        if len(new_prefix) > 5:
            return await send_error_embed(ctx, "Invalid Prefix", "The prefix cannot be longer than 5 characters.")
        
        # Direct motor usage: access collection
        guild_config_collection = self.db.guild_configs # Access the collection
        
        # Find or create the guild config document
        existing_config = await guild_config_collection.find_one({'guild_id': ctx.guild.id})
        
        if not existing_config:
            # Insert a new document
            new_config = {
                'guild_id': ctx.guild.id,
                'prefix': new_prefix,
                # ... other default settings if any
            }
            await guild_config_collection.insert_one(new_config)
        else:
            # Update existing document
            await guild_config_collection.update_one(
                {'guild_id': ctx.guild.id},
                {'$set': {'prefix': new_prefix}}
            )

        await send_success_embed(
            ctx,
            "Prefix Updated",
            f"The bot's prefix for this server has been set to `{new_prefix}`."
        )

    @commands.hybrid_command(
        name="currentprefix",
        description="Shows the current prefix for this server."
    )
    async def currentprefix(self, ctx: commands.Context):
        guild_config_collection = self.db.guild_configs
        config_doc = await guild_config_collection.find_one({'guild_id': ctx.guild.id})
        
        current_prefix = config_doc['prefix'] if config_doc and 'prefix' in config_doc else self.bot.command_prefix.get_default_prefix() # Fallback
        
        await send_info_embed(
            ctx,
            "Current Prefix",
            f"The current prefix for this server is `{current_prefix}`."
        )

async def setup(bot):
    await bot.add_cog(Settings(bot))

import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio # For the health check server
from aiohttp import web # For the health check server

# For local .env file loading (not used on Render directly, but good for local dev)
from dotenv import load_dotenv
load_dotenv()

# --- Configuration Variables (from environment) ---
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX', '!') # Default to '!' if not set
OWNER_ID = int(os.getenv('BOT_OWNER_ID')) if os.getenv('BOT_OWNER_ID') else None
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('MONGO_DB_NAME', 'your_bot_db') # Default DB name

# --- MongoDB Setup (will be initialized in on_ready) ---
import motor.motor_asyncio
from beanie import init_beanie
from models import GuildConfig, UserProfile, Reminder, ModCase, CustomCommand # Import all your models here!

# --- Intents Setup ---
intents = discord.Intents.default()
intents.message_content = True # Required for prefix commands, leveling, etc.
intents.members = True       # Required for member-related events (joins, leaves, moderation)
intents.presences = True     # Required for presence tracking (if you need it)

# --- Custom Prefix Resolver ---
async def get_prefix(bot, message):
    if message.author.id == OWNER_ID:
        return commands.when_mentioned_or("")(bot, message) # Owner can use no prefix or mention
    
    if message.guild:
        config = await GuildConfig.find_one(GuildConfig.guild_id == message.guild.id)
        if config and config.prefix:
            return commands.when_mentioned_or(config.prefix)(bot, message)
            
    return commands.when_mentioned_or(PREFIX)(bot, message)

# --- Bot Initialization ---
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

# --- Bot Events ---
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    
    # --- Set Bot Status and Activity ---
    # Activity: Streaming "Your Mom" with a placeholder URL (Discord requires a valid URL for streaming)
    # Status: Do Not Disturb (dnd)
    streaming_url = "https://www.twitch.tv/discord" # Placeholder, Discord requires a valid URL for streaming to show properly
    await bot.change_presence(
        activity=discord.Streaming(name="Your Mom", url=streaming_url),
        status=discord.Status.dnd # Set status to Do Not Disturb
    )
    print("Bot status set to DND, streaming 'Your Mom'.")

    # Initialize MongoDB connection
    if MONGO_URI:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
        await init_beanie(database=client[DB_NAME], document_models=[
            GuildConfig, 
            UserProfile, 
            Reminder,
            ModCase,
            CustomCommand,
            # Add all other Beanie Document models here!
        ])
        print(f"Connected to MongoDB database: {DB_NAME}")
    else:
        print("MONGO_URI environment variable not set. Cannot connect to MongoDB.")
        # Consider handling this case (e.g., exiting or running in a limited, non-persistent mode)
        
    # Load cogs
    print("Loading cogs...")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'): # Exclude __init__.py
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"Loaded cog: {filename[:-3]}")
            except Exception as e:
                print(f"Failed to load cog {filename[:-3]}: {e}")
    print("All cogs loaded!")

    # Sync slash commands
    # Use guild sync for faster testing during development:
    # guild = discord.Object(id=YOUR_TEST_GUILD_ID) # Replace with your test guild ID
    # bot.tree.copy_global_to(guild=guild)
    # await bot.tree.sync(guild=guild)
    
    # For production, use global sync (might take up to an hour for Discord to update):
    await bot.tree.sync()
    print("Slash commands synced!")

    # --- Render Health Check Web Server (for free tier uptime) ---
    port = int(os.getenv('PORT', 8000)) # Render provides PORT env var
    app = web.Application()
    app.router.add_get('/', lambda r: web.Response(text="Bot is alive!"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Health check web server started on port {port}")

@bot.event
async def on_command_error(ctx, error):
    from utils import send_error_embed # Import here to avoid circular dependencies

    if isinstance(error, commands.CommandNotFound):
        # Ignore if command not found, or send a subtle error embed
        return 
    
    elif isinstance(error, commands.MissingRequiredArgument):
        await send_error_embed(
            ctx,
            "Missing Argument",
            f"You're missing a required argument for this command. \nUsage: `{bot.command_prefix}{ctx.command.name} {ctx.command.signature}`"
        )
    elif isinstance(error, commands.BadArgument):
         await send_error_embed(
            ctx,
            "Invalid Argument",
            f"One of your arguments was invalid. \nUsage: `{bot.command_prefix}{ctx.command.name} {ctx.command.signature}`"
        )
    elif isinstance(error, commands.MissingPermissions) or isinstance(error, commands.MissingRole):
        await send_error_embed(
            ctx,
            "Permission Denied",
            "You don't have the necessary permissions to use this command."
        )
    elif isinstance(error, commands.BotMissingPermissions) or isinstance(error, commands.BotMissingRole):
        await send_error_embed(
            ctx,
            "Bot Lacks Permissions",
            f"I need the following permissions to run this command: `{'`, `'.join(error.missing_permissions)}`."
        )
    elif isinstance(error, commands.NoPrivateMessage):
        await send_error_embed(ctx, "DM Not Allowed", "This command cannot be used in private messages.")
    else:
        # Catch-all for other errors
        print(f"Unhandled error in command {ctx.command.name}: {error}") # Log to console for debugging
        await send_error_embed(
            ctx,
            "An Unexpected Error Occurred",
            f"Something went wrong while trying to execute that command. Please try again later. If the problem persists, contact the bot owner ({bot.get_user(OWNER_ID).mention if OWNER_ID else 'Bot Owner'})."
        )


# --- Run the Bot ---
if TOKEN and OWNER_ID is not None and MONGO_URI: # OWNER_ID can be 0, so check for not None
    bot.run(TOKEN)
else:
    print("Error: Missing one or more required environment variables (DISCORD_TOKEN, BOT_OWNER_ID, MONGO_URI).")
    print("Please check your .env file or Render environment settings.")

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, slash_command, ApplicationContext # Use the py-cord way
import os
import asyncio
from aiohttp import web

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX', '!')
OWNER_ID = int(os.getenv('BOT_OWNER_ID')) if os.getenv('BOT_OWNER_ID') else None
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('MONGO_DB_NAME', 'your_bot_db')

# --- MongoDB Setup (will use motor directly) ---
import motor.motor_asyncio
# from beanie import init_beanie # <-- REMOVE THIS
# from models import GuildConfig, UserProfile, Reminder, ModCase, CustomCommand # <-- REMOVE or adjust this import

# You'll need to define a global db client or pass it around
mongo_client = None
db = None

# --- Intents Setup ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

# --- Custom Prefix Resolver ---
async def get_prefix(bot, message):
    if message.author.id == OWNER_ID:
        return commands.when_mentioned_or("")(bot, message)
    
    if message.guild and db: # Check if db is initialized
        # Direct motor usage: access collection
        guild_config_doc = await db.guild_configs.find_one({'guild_id': message.guild.id})
        if guild_config_doc and guild_config_doc.get('prefix'):
            return commands.when_mentioned_or(guild_config_doc['prefix'])(bot, message)
            
    return commands.when_mentioned_or(PREFIX)(bot, message)

bot = commands.Bot(command_prefix=get_prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    
    streaming_url = "https://www.twitch.tv/discord"
    await bot.change_presence(
        activity=discord.Streaming(name="Your Mom", url=streaming_url),
        status=discord.Status.dnd
    )
    print("Bot status set to DND, streaming 'Your Mom'.")

    # Initialize MongoDB connection (motor direct)
    global mongo_client, db # Access global variables
    if MONGO_URI:
        mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
        db = mongo_client[DB_NAME] # Get the database object
        print(f"Connected to MongoDB database: {DB_NAME}")
        # NO init_beanie CALL HERE
    else:
        print("MONGO_URI environment variable not set. Cannot connect to MongoDB.")
        
    print("Loading cogs...")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                # Pass the db object to cogs if they need it directly
                # await bot.load_extension(f'cogs.{filename[:-3]}', db=db) # You'd adjust cog setup for this
                await bot.load_extension(f'cogs.{filename[:-3]}') # For now, assume cogs will get db via bot.db
                print(f"Loaded cog: {filename[:-3]}")
            except Exception as e:
                print(f"Failed to load cog {filename[:-3]}: {e}")
    print("All cogs loaded!")

    # Attach db to bot object for easy access in cogs
    bot.mongo_client = mongo_client
    bot.db = db

    await bot.tree.sync()
    print("Slash commands synced!")

    port = int(os.getenv('PORT', 8000))
    app = web.Application()
    app.router.add_get('/', lambda r: web.Response(text="Bot is alive!"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Health check web server started on port {port}")

@bot.event
async def on_command_error(ctx, error):
    from utils import send_error_embed 

    if isinstance(error, commands.CommandNotFound):
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
        print(f"Unhandled error in command {ctx.command.name}: {error}")
        await send_error_embed(
            ctx,
            "An Unexpected Error Occurred",
            f"Something went wrong while trying to execute that command. Please try again later. If the problem persists, contact the bot owner ({bot.get_user(OWNER_ID).mention if OWNER_ID else 'Bot Owner'})."
        )


if TOKEN and OWNER_ID is not None and MONGO_URI:
    bot.run(TOKEN)
else:
    print("Error: Missing one or more required environment variables (DISCORD_TOKEN, BOT_OWNER_ID, MONGO_URI).")
    print("Please check your .env file or Render environment settings.")

import os
import discord
from discord import app_commands
import discord.ext import commands
from dotenv import load_dotenv
from utils import info_embed, error_embed, success_embed

OWNER_ID = int(os.getenv("BOT_OWNER_ID"))  # from railway variables
PREFIX = os.getenv("BOT_PREFIX")  # from railway variables

INFO_EMOJI = "<:warningicon:1426788199598133289>"

class General(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

@app_commands.command(name="ping",description="Check the bot's response time")
async def slash_ping(self, inetraction: dicord.Interation):
  start_time = time.time()
  await
  interaction.response.defer(thinking=True)

latency = round(self.bot.latency * 1000)
end_time = round(time.time() - start_time) * 1000)

embed = info_embed("{INFO_EMOJI} Pong !", f"Latency : `{latency}ms`", interaction.user)
await
ineteraction.response.send_message(embed=embed)

@commands.command(name="ping")
async def ping(self, ctx):
  latency = round(self.bot.latency *1000)
  embed = info_embed("{INFO_EMOJI} Pong !", f"Latency : `{latency}ms`", ctx.author)
  await ctx.send(embed=embed)

  @commands.Cog.listener()
  async def on_message(self, message: discord.Message):
    if message.author.bot:
      return

if message.author.id == OWNER_ID 
and message.content.lower() == "Ping":
latency = 
round(self.bot.latency * 1000)
embed = info-embed("{INFO_EMOJI} Pong !",
                   f"Latency : `{latency}ms`",message.author)
await
message.channel.send(embed=embed)

async def setup(bot):
  await bot.add_cog(General(bot))

                        

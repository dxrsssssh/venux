import discord
from discord import app_commands
import discord.ext import commands
import time
import os

OWNER_ID = int(os.getenv("BOT_OWNER_ID"))  # from railway variables
PREFIX = os.getenv("BOT_PREFIX")  # from railway variables

INFO_EMOJI = "<:warningicon:1426788199598133289>"

class Ping(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

@app_commands.command(name="ping",description="Check the bot's response time")
async def ping(self, inetraction:dicord.Interation):
  start_time = time.time()
  await
  interaction.response.defer(thinking=True)

latency = round(self.bot.latency * 1000)
end_time = round(time.time() - start_time) * 1000)

# EMBED CONFIGURATION 
gradient_color = discord.Color.from_rgb(88, 101, 242)

embed = discord.Embed(title=f"{INFO_EMOJI} **Pong!**",
                      description="> _System performance metrics:_",
                      color=gradient_color
                     )
embed.add_field(
  name=f"{INFO_EMOJI} **Websocket Latency**",
  value=f"```yaml\n{end_time}ms\n```",
  inline=True
)
embed.add_field(
  name=" ",  # invisible spacing
  value="> 8Bot is fully operational and stable.*",
  inline=False
)

embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
embed.set_footer(
  text=f"Requested by {interaction.user.name}",

  icon_url=interaction.user.avatar.url is interaction.user.avatar else None
)
embed.timestamp = discord.utils.utcnow()

await
interaction.followup.send(embed=embed0

                          async def setup(bot):
                            await bot.add_cog(Ping(bot))

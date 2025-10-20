# utils.py
import discord

# EMBED COLORS
COLORS = {
  "success": discord.Color.green(),
  "error": discord.Color.red(),
  "info": discord.Color.blue(),
  "warning": discord.Color.orange()
}

# FOOTERS
def success_embed(title: str, description: str, user: discord.User):
  embed = discord.Embed(
    title=title,
    description=description,
    color=COLORS["success"]
  )
  embed.set_footer(text=f"Requested by {user}", icon_url=user.display_avatar.url)
  return embed

def error_embed(title: str, description: str, user: discord.User):
  embed = discord,Embed(
    title=title,
    description=description,
    color=COLORS["error"]
  )
  embed.set_footer(text=f"Requested bt {user}", icon_url=user.display_avatar.url)
  return embed

  def info_embed(title: str, description: str, user: discord.User):
    embed = discord.Embed(
      title=title,
      description=description,
      color=COLORS["info"]
    )
    embed.set_footer(text=f"Requested by {user}", icon_url=user.display_avatar.url)
    return embed
                

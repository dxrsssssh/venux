# utils.py
import discord
from config import EMOJIS, BOT_HEX_COLOR # Import emojis and bot color from config

async def create_embed(ctx: commands.Context, title: str, description: str, color: discord.Color = BOT_HEX_COLOR, 
                       thumbnail_url: str = None, image_url: str = None, 
                       fields: list = None, author_name: str = None, 
                       author_icon_url: str = None, show_footer: bool = True) -> discord.Embed:
    """
    Creates a consistently styled Discord embed.

    Args:
        ctx: The command context.
        title: The title of the embed.
        description: The main content of the embed.
        color: The color of the embed (defaults to BOT_HEX_COLOR).
        thumbnail_url: URL for the embed's thumbnail.
        image_url: URL for the embed's main image.
        fields: A list of tuples (name, value, inline) for embed fields.
        author_name: Name for the embed author.
        author_icon_url: Icon URL for the embed author.
        show_footer: Whether to include the default bot footer.

    Returns:
        A discord.Embed object.
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=discord.utils.utcnow()
    )

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)
    if image_url:
        embed.set_image(url=image_url)
    if fields:
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
    
    if author_name and author_icon_url:
        embed.set_author(name=author_name, icon_url=author_icon_url)

    if show_footer:
        # Use ctx.author.display_avatar.url for more robust avatar fetching
        embed.set_footer(text=f"{ctx.bot.user.name} | Requested by {ctx.author.display_name}", 
                         icon_url=ctx.bot.user.avatar.url if ctx.bot.user.avatar else None)

    return embed

async def send_success_embed(ctx: commands.Context, title: str, description: str, **kwargs):
    """Sends a green success embed with a checkmark emoji."""
    embed = await create_embed(ctx, f"{EMOJIS.get('success', '')} {title}", description, discord.Color.green(), **kwargs)
    await ctx.send(embed=embed)

async def send_error_embed(ctx: commands.Context, title: str, description: str, **kwargs):
    """Sends a red error embed with an X emoji."""
    embed = await create_embed(ctx, f"{EMOJIS.get('error', '')} {title}", description, discord.Color.red(), **kwargs)
    await ctx.send(embed=embed)

async def send_warning_embed(ctx: commands.Context, title: str, description: str, **kwargs):
    """Sends an orange warning embed with a warning emoji."""
    embed = await create_embed(ctx, f"{EMOJIS.get('warning', '')} {title}", description, discord.Color.orange(), **kwargs)
    await ctx.send(embed=embed)

async def send_info_embed(ctx: commands.Context, title: str, description: str, **kwargs):
    """Sends a general info embed (default bot color) with an info emoji."""
    embed = await create_embed(ctx, f"{EMOJIS.get('info', '')} {title}", description, BOT_HEX_COLOR, **kwargs)
    await ctx.send(embed=embed)

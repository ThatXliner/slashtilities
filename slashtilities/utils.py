import asyncio
import datetime
import platform
import random
import sys
from typing import Optional, Tuple, Union

import discord
from discord.ext.commands import Context
from discord_slash.context import SlashContext

from slashtilities import log


async def get_last_message_from(
    context: Union[SlashContext, Context]
    # author: discord.Member, channel: discord.TextChannel
) -> Optional[str]:
    log.info("Getting last message")
    try:
        output = None
        if isinstance(context, SlashContext):
            output = await asyncio.wait_for(
                context.channel.history(limit=None).get(author__id=context.author.id),
                timeout=10.0,
            )  # Timeout after 10 seconds
        else:
            async for message in context.channel.history(limit=None):
                if message.id == context.message.id:
                    continue
                if message.author.id == context.author.id:
                    output = message
                    break
    except asyncio.TimeoutError:
        log.info("Timed out")
        raise
    else:
        if output is None:
            log.info("Not found")
        else:
            log.info("Found")
        return output


async def errorize(error_msg: str) -> discord.Embed:
    log.error(error_msg)
    return discord.Embed(
        title=":x: Error",
        description=error_msg,
        color=discord.Color.red(),
    )


async def joke_info() -> str:
    jokes: Tuple[str, ...] = (
        "Uses Heroku: True",
        "Is a cool bot: True",
        "Hosted on GitHub: True",
        "Implemented via Python: True",
        "Implemented via NodeJS: False",
        "Hosted on BitBucket: False",
        "Hosted on GitLab: False",
        "Breaks easily: False",
    )
    return random.choice(jokes)


async def get_os() -> str:
    # TODO: Cygwin too
    if sys.platform.startswith("win"):
        version = platform.win32_ver()[0]
    elif sys.platform.startswith("darwin"):
        version = platform.mac_ver()[0]
    else:  # TODO: Linux
        version = "Unknown"
    return f"{platform.system()}, {version}"


async def get_python_version() -> str:
    return f"{platform.python_version()}, on {platform.system()}"


async def get_timestamp() -> str:  # TODO: Heroku-style timestamps
    return await basically_today("{}")


async def disable(ctx, why: str = "The devs have not given why") -> None:
    await ctx.send(
        embed=discord.Embed(
            title=":warning: This command is disabled",
            description=why,
            color=discord.Color.orange(),
        ).set_footer(text="Yeah, sorry")
    )


async def send_hidden_message(ctx, msg: str) -> None:
    try:
        await ctx.send(msg, hidden=True)
    except TypeError:
        await ctx.send(msg, delete_after=5)
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass


async def quote(msg: str) -> str:
    output = ""
    for line in msg.splitlines():
        output += "> " + line
    return output


async def basically_today(msg_format: str) -> str:
    log.info(f"Sending today's time to format {msg_format!r}")
    return msg_format.format(
        datetime.datetime.today().strftime("%B, %d, %Y (%m/%d/%Y)")
    )


NO_MENTIONS = discord.AllowedMentions.none()

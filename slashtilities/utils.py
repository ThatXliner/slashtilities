import datetime
from typing import Optional

import discord
from discord.ext import commands
from slashtilities import log


async def get_last_message_from(
    author: discord.Member, channel: discord.TextChannel
) -> Optional[str]:
    log.info("Getting last message")
    async for message in channel.history(oldest_first=False, limit=None):
        if message.author == author:
            log.info("Success")
            return message
    log.info("Not found")
    return None


async def errorize(error_msg: str) -> discord.Embed:
    log.error(error_msg)
    return discord.Embed(
        title=":x: Error",
        description=error_msg,
        color=discord.Color.red(),
    )


async def disable(ctx, why: str = "The devs have not given why") -> None:
    await ctx.send(
        embed=discord.Embed(
            title=":warning: This command is disabled",
            description=why,
            color=discord.Color.orange(),
        ).set_footer(text="Yeah, sorry")
    )


async def quote(msg: str) -> str:
    output = ""
    for line in msg.splitlines():
        output += "> " + line
    return output


async def basically_today(msg_format: str) -> str:
    log.info(f"Sending today's time to format {msg_format!r}")
    return msg_format.format(
        datetime.datetime.today().strftime("%B, %d, %Y (%m/%d/%Y) %I:%M")
    )

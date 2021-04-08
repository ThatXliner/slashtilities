import datetime
from typing import Optional

import discord
from discord.ext import commands


async def get_last_message_from(
    author: discord.Member, channel: discord.TextChannel
) -> Optional[str]:
    print("Getting last message...", end=" ")
    async for message in channel.history(oldest_first=False, limit=None):
        if message.author.id == author.id:
            print("\N{WHITE HEAVY CHECK MARK} found")
            return message
    print("\N{CROSS MARK} Not found")
    return None


async def errorize(ctx: commands.Context) -> None:
    await ctx.send(
        embed=discord.Embed(
            title=":x: Error",
            description=(
                "How do you expect me to find your last message if "
                "I don't even have access to this channel???"
            ),
            color=discord.Color.red(),
        ).set_footer(text="What an idiot")
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
    return msg_format.format(
        datetime.datetime.today().strftime("%B, %d, %Y (%m/%d/%Y) %I:%M %p")
    )

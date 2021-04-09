from collections import defaultdict
from typing import DefaultDict, List

import discord
from discord.ext import commands
from disputils import BotEmbedPaginator
from slashtilities import utils


async def make_list(stuff: List[str]) -> str:
    output = ""
    for item in stuff:
        output += f" - [**Jump to message**]({item})\n"
    return output


async def igotpinged(ctx: commands.Context) -> None:
    await ctx.defer()
    try:
        last_msg = await utils.get_last_message_from(ctx.author, channel=ctx.channel)
    except discord.errors.Forbidden:
        await ctx.send(
            embed=utils.errorize(
                "How do you expect me to find your last message if "
                "I don't even have access to this channel???",
            ).set_footer(text="What an idiot")
        )
    else:
        print("Getting last ping...", end=" ")
        if last_msg is None:
            await ctx.send(
                utils.errorize(
                    "Couldn't find your last message (maybe you didn't send any messages)"
                )
            )
            print("Error")
            return
        ping_msgs = [
            message
            async for message in ctx.channel.history(
                after=last_msg,
                limit=None,  # or 9000?
            )
            if ctx.author.mentioned_in(message)
        ]

        if len(ping_msgs) > 0:
            print("\N{WHITE HEAVY CHECK MARK}")
            if len(ping_msgs) > 1:
                to_paginate = [
                    discord.Embed(
                        title=":mag: Found!",
                        description="Click on the pagination buttons to see\n"
                        "who pinged you (times out *after 100 seconds*)",
                        color=discord.Color.green(),
                    ).add_field(
                        name="Your last message",
                        value=f"[**Jump to message**]({last_msg.jump_url})",
                        inline=False,
                    )
                ]
                author_and_pings: DefaultDict[discord.Member, List[str]] = defaultdict(
                    list
                )
                for message in ping_msgs:
                    author_and_pings[message.author].append(message.jump_url)
                to_paginate.extend(
                    [
                        discord.Embed(
                            title=f"",
                            description=await make_list(msgs),
                            color=discord.Color.green(),
                        ).set_author(
                            name=f"{author} pinged you in these messages:",
                            icon_url=str(author.avatar_url),
                        )
                        for author, msgs in author_and_pings.items()
                    ]
                )
                paginator = BotEmbedPaginator(ctx, to_paginate)
                await paginator.run(
                    channel=ctx  # Very hacky. It'll think ctx.send == channel.send
                )  # But it works
            else:
                await ctx.send(
                    embed=(
                        discord.Embed(
                            title=":mag: Found!",
                            description=f"{ping_msgs[0].author.mention} pinged you [**here**]({ping_msgs[0].jump_url})\n\n[**Your last message**]({last_msg.jump_url})",
                            color=discord.Color.green(),
                        )
                    )
                )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title=":ghost: Not found!",
                    description=f"I didn't find anyone. You probably got ***ghost pinged***\n\n[**Your last message**]({last_msg.jump_url})",
                    color=discord.Color.red(),
                ).set_footer(text="Imagine ghost pinging")
            )
    print("END OF `igotpinged`")

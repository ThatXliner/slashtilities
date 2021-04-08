import discord
from discord.ext import commands
from slashtilities import utils


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
                to_send = discord.Embed(
                    title=":mag: Found!",
                    description="The following people did:",
                    color=discord.Color.green(),
                ).add_field(
                    name="Your last message",
                    value=f"[**Jump to message**]({last_msg.jump_url})",
                    inline=False,
                )
                for message in ping_msgs:
                    to_send.add_field(
                        name=message.author,
                        value=f"[**Jump to message**]({message.jump_url})",
                        inline=False,
                    )
                await ctx.send(embed=to_send)
            else:
                await ctx.send(
                    embed=(
                        discord.Embed(
                            title=":mag: Found!",
                            description=f"{ping_msgs[0].author.mention} pinged you [**here**]({ping_msgs[0].jump_url})\n[**Your last message**]({last_msg.jump_url})",
                            color=discord.Color.green(),
                        )
                    )
                )
        else:
            print("\N{GHOST}")
            await ctx.send(
                embed=discord.Embed(
                    title=":ghost: Not found! D:",
                    description=f"I didn't find anyone. You probably got ***ghost pinged***\n[**Your last message**]({last_msg.jump_url})",
                    color=discord.Color.red(),
                ).set_footer(text="Imagine ghost pinging")
            )
    print("END OF `igotpinged`")

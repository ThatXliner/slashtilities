# TODO: Use embeds
import asyncio
import os

import discord
from discord import Color, Embed
from discord_slash import SlashCommand  # Importing the newly installed library.
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option, remove_all_commands
from slashtilities import cc, igotpinged, meta, polling

TOKEN = os.environ["DISCORD_TOKEN"]
intents = discord.Intents().default()
client = discord.Client(
    intents=intents,
    activity=discord.Activity(
        type=discord.ActivityType.watching, name="your every step >:)"
    ),
)
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    print("\N{WHITE HEAVY CHECK MARK} I am ready!")


def get_testing_guilds():
    if os.environ.get("DISCORD_TEST_GUILDS") is not None:
        return os.environ["DISCORD_TEST_GUILDS"].split(",") or None
    else:
        return None


# if os.environ.get("DISCORD_TESTING") == "1":
#     return os.environ["DISCORD_TEST_GUILDS"].split(",") or None
# else:
#     return None


@slash.slash(
    name="ping",
    description="Return the latency of the bot",
    guild_ids=get_testing_guilds(),
)
async def ping(ctx):
    gotten_ping = client.latency * 1000
    print(f"Recorded ping: {gotten_ping} ms")
    await ctx.send(
        embed=Embed(
            title=":ping_pong: Pong!",
            description=f"{gotten_ping:.4} ms",
            color=Color.blue(),
        )
    )


slash.add_slash_command(
    igotpinged.igotpinged,
    name="igotpinged",  # TODO: Add "whopingedme" alias
    description="Get the person who pinged you ever since your last message",
    guild_ids=get_testing_guilds(),
)
slash.add_slash_command(
    cc.cc,
    name="cc",
    description="CC other people your last message",
    guild_ids=get_testing_guilds(),
    options=cc.create_person_options(10),
)
slash.add_slash_command(
    cc.bcc,
    name="bcc",
    description="BCC other people your last message",
    guild_ids=get_testing_guilds(),
    options=cc.create_person_options(10),
)
slash.add_slash_command(
    polling.poll,
    name="poll",
    description="Send a multi-choice poll (not mutually exclusive)",
    guild_ids=get_testing_guilds(),
    options=polling.create_poll_options(10),
)
slash.add_slash_command(
    polling.yesno,
    name="yesno",
    description="Send a yes-or-no question (not mutually exclusive)",
    guild_ids=get_testing_guilds(),
    options=[
        create_option(
            "question",
            "The question you're going to ask",
            option_type=SlashCommandOptionType.STRING,
            required=True,
        ),
    ],
)
slash.add_slash_command(
    meta.invite,
    name="invite",
    description="Our bot's invite links!",
    guild_ids=get_testing_guilds(),
)
slash.add_slash_command(
    meta.vote,
    name="vote",
    description="Vote for our bot here!",
    guild_ids=get_testing_guilds(),
)

# Commented out because should be a mod-only command
# @slash.slash(
#     name="purge",
#     description="Deletes some messages",
#     options=[
#         create_option(
#             name="amount",
#             description="The amount of messages to delete (defaults to 100)",
#             option_type=SlashCommandOptionType.INTEGER,
#             required=False,
#         )
#     ],
# )
# async def purge(ctx, amount: int = 100):
#     await ctx.send(
#         f":broom: Purged {len(await ctx.channel.purge(limit=amount))} messages"
#     )


if __name__ == "__main__":
    client.run(TOKEN)

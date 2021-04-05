# TODO: Use embeds
import os

import discord
import discord.ext.commands
from discord_slash import SlashCommand  # Importing the newly installed library.

# from discord_slash.model import SlashCommandOptionType
# from discord_slash.utils.manage_commands import create_option

TOKEN = os.environ["DISCORD_TOKEN"]
intents = discord.Intents().default()
client = discord.Client(intents=intents, activity=discord.Game("Listening to summons"))
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    print("\N{WHITE HEAVY CHECK MARK} I am ready!")


def get_testing_guilds():
    if os.environ.get("DISCORD_TESTING") == "1":
        return os.environ["DISCORD_TEST_GUILDS"].split(",")
    else:
        return None


@slash.slash(
    name="ping",
    description="Return the latency of the bot",
    guild_ids=get_testing_guilds(),
)
async def ping(ctx):
    gotten_ping = client.latency * 1000
    print(f"Recorded ping: {gotten_ping} ms")
    await ctx.send(f":ping_pong: Pong! | (`{gotten_ping:.4}` ms)")


@slash.slash(
    name="igotpinged",  # TODO: Add "whopingedme" alias
    description="Get the person who pinged you ever since your last message",
    guild_ids=get_testing_guilds(),
)
async def igotpinged(ctx):
    ctx.defer()
    try:
        last_msg = await get_last_message_from(ctx.author, channel=ctx.channel)
    except discord.errors.Forbidden:
        await ctx.send(
            ":x: How do you expect me to find your last message if "
            "I don't even have access to this channel???"
        )
    else:
        print("Getting last ping...", end=" ")
        async for message in ctx.channel.history(
            after=last_msg,
            limit=None,  # or 9000?
        ):
            if ctx.author.mentioned_in(message):
                print("\N{WHITE HEAVY CHECK MARK}")
                await ctx.send(
                    f":mag: {message.author} did, right here: {message.jump_url}"
                )
                break
        else:
            print("\N{GHOST}")
            await ctx.send(
                ":ghost: I didn't find anyone. You probably got ***ghost pinged***"
            )
    print("END OF `igotpinged`")


async def get_last_message_from(author, channel):
    print("Getting last message...", end=" ")
    async for message in channel.history(oldest_first=False, limit=None):
        if message.author.id == author.id:
            print("\N{WHITE HEAVY CHECK MARK} found")
            return message
    print("\N{CROSS MARK} Not found")
    return None


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

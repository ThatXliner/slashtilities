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


@slash.slash(name="ping", description="Return the latency of the bot")
async def ping(ctx):
    await ctx.send(f":ping_pong: Pong! | (`{client.latency*1000:.4}` ms)")


@slash.slash(
    name="igotpinged",  # TODO: Add "whopingedme" alias
    description="Get the person who pinged you ever since your last message",
)
async def igotpinged(ctx):
    last_msg = await get_last_message_from(ctx.author, channel=ctx.channel)
    async with ctx.channel.typing():
        async for message in ctx.channel.history(
            after=last_msg,
            limit=None,  # or 9000?
        ):
            if ctx.author.mentioned_in(message):
                await ctx.send(
                    f":mag: {message.author} did, right here: {message.jump_url}"
                )
                break
        else:
            await ctx.send(
                ":ghost: I didn't find anyone. You probably got ***ghost pinged***"
            )


async def get_last_message_from(author, channel):
    async for message in channel.history(oldest_first=False, limit=None):
        if message.author.id == author.id:
            return message
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

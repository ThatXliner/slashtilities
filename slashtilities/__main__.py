# TODO: Use embeds
import os
import traceback

import discord
from discord import Color, Embed, Intents
from discord.ext.commands import Bot, when_mentioned_or

# Importing the newly installed library.
from discord_slash import SlashCommand

from slashtilities import cogs, igotpinged, log, utils

TOKEN = os.environ["DISCORD_TOKEN"]
intents = Intents().default()

bot = Bot(
    when_mentioned_or("/"),
    intents=intents,
    activity=discord.Activity(
        type=discord.ActivityType.watching, name="@ThatXliner#1995 code me"
    ),
)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print("\N{WHITE HEAVY CHECK MARK} I am ready!")


@bot.event
async def on_slash_command_error(ctx, exception):
    log.critical(
        "\n".join(
            traceback.format_exception(
                type(exception), exception, exception.__traceback__
            )
        )
    )
    to_send = (
        discord.Embed(
            title=":boom: CRITICAL!!!",
            description="😱 AHHHHHHH!!! AN ***UNCAUGHT EXCEPTION!!!***",
            color=discord.Color.red(),
        )
        .add_field(
            name=":bug: You should tell us about this",
            value="Go to the "
            "[issue tracker](https://github.com/ThatXliner/slashtilities/issues) to do that.\n"
            "Make sure to screenshot/link/keep this message because "
            "the information below is very valuable for debugging.",
        )
        .add_field(
            name="Exception", value="```py\n" + repr(exception) + "\n```", inline=False
        )
        .add_field(
            name="Traceback",
            value="```py\n"
            + "\n".join(
                traceback.format_exception(
                    type(exception), exception, exception.__traceback__
                )
            )
            + "\n```",
            inline=False,
        )
        .add_field(
            name="Miscellenous Information",
            value=f"The bug-finder: {ctx.author.mention}\n"
            + "Python version: "
            + await utils.get_python_version()
            + "\n"
            + "Operating System: "
            + await utils.get_os()
            + "\n"
            + f"Command: {ctx.command}\n"
            "Timestamp: " + await utils.get_timestamp(),
        )
        .set_footer(text="😓 sorry.")
    )
    try:
        await ctx.channel.send(
            embed=to_send,
            allowed_mentions=discord.AllowedMentions().none(),
        )
    except:
        await ctx.send(
            (
                "😱 AHHHHHHH!!! AN ***UNCAUGHT EXCEPTION!!!***\n"
                ":bug: You should tell us about this\n"
                "Go to the [issue tracker](https://github.com/ThatXliner/slashtilities/issues) to do that.\n"
                "Make sure to screenshot/link/keep this message because "
                "the information below is very valuable for debugging.\n\n"
                "Traceback:\n"
                "```py\n"
                + "\n".join(
                    traceback.format_exception(
                        type(exception), exception, exception.__traceback__
                    )
                )
                + "\n```"
            ),
            allowed_mentions=discord.AllowedMentions().none(),
        )


# if os.environ.get("DISCORD_TESTING") == "1":
#     return os.environ["DISCORD_TEST_GUILDS"].split(",") or None
# else:
#     return None


@slash.slash(
    name="ping",
    description="Return the latency of the bot",
)
async def ping(ctx):
    gotten_ping = bot.latency * 1000
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
)
bot.add_cog(cogs.Meta(bot))
bot.add_cog(cogs.Polling(bot))
bot.add_cog(cogs.CCing(bot))
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
    bot.run(TOKEN)

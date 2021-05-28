import os
import traceback

import discord
from discord import Intents
from discord.ext.commands import Bot, when_mentioned_or

# Importing the newly installed library.
from discord_slash import SlashCommand

from slashtilities import cogs, log, utils

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
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    # TODO: Replace "bot" with *this bot*
    # Check if reacting to a message a bot has reacted to

    if not any(
        [
            (await other_reactions.users().find(lambda reactor: reactor.bot))
            for other_reactions in reaction.message.reactions
        ]
    ):
        return
    # Check if a user is not reacting to the bot-given reaction...
    if (not user.bot) and await reaction.users().find(lambda user: user.bot) is None:
        # Then remove that reaction
        try:
            await reaction.remove(user)
        except discord.errors.Forbidden:
            pass  # Fail silently because this should work unnoticed, in the background
        # Why? I hate it when trolls do something like
        # add a ":three:" reaction to a 2-option poll
        # no more trolls!


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent) -> None:
    if payload.user_id == bot.user.id:
        channel = bot.get_channel(payload.channel_id)
        assert isinstance(channel, discord.TextChannel)
        message = channel.get_partial_message(payload.message_id)
        await message.add_reaction(payload.emoji)


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


bot.add_cog(cogs.Meta(bot))
bot.add_cog(cogs.Polling(bot))
bot.add_cog(cogs.CCing(bot))
bot.add_cog(cogs.Misc(bot))
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

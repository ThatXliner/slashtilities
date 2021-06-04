import os
import traceback

import discord
from discord import Intents
from discord.ext.commands import Bot, when_mentioned_or

# Importing the newly installed library.
from discord_slash import SlashCommand

from slashtilities import background, cogs, log, utils

TOKEN = os.environ["DISCORD_TOKEN"]
intents = Intents().default()

bot = Bot(when_mentioned_or("/"), intents=intents)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    message = await bot.get_channel(payload.channel_id).fetch_message(
        payload.message_id
    )
    reactions = message.reactions
    # Check if reacting to a message a bot has reacted to
    if not any((other_reactions.me for other_reactions in reactions)):
        return

    # Check if a user is not reacting to the bot-given reaction...
    if not payload.user_id == bot.user.id:
        if str(payload.emoji) not in {
            str(reaction.emoji) for reaction in reactions if reaction.me
        }:
            # Then remove that reaction
            try:
                await message.remove_reaction(
                    payload.emoji, payload.member or bot.get_user(payload.user_id)
                )
            except discord.errors.Forbidden:
                pass  # Fail silently because this should work unnoticed, in the background
            # Why? I hate it when trolls do something like
            # add a ":three:" reaction to a 2-option poll
            # no more trolls!
        # Or... check for mutually exclusive stuff!
        elif str(payload.emoji) in {
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
            "🔟",
            "👍",
            "👎",
        }:  # Why the list? For future proofing
            for reaction in reactions:
                if reaction.emoji != payload.emoji and await reaction.users().get(
                    id=payload.user_id
                ):
                    # Remove old reaction that is
                    # 1. not the same as the new reaction
                    # 2. from the same author
                    await message.remove_reaction(
                        reaction.emoji,
                        payload.member or bot.get_user(payload.user_id),
                    )
                    break


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent) -> None:
    if payload.user_id == bot.user.id:
        channel = bot.get_channel(payload.channel_id)
        assert isinstance(channel, discord.TextChannel)
        message = channel.get_partial_message(payload.message_id)
        await message.add_reaction(payload.emoji)


@bot.event
async def on_ready():
    log.info("\N{WHITE HEAVY CHECK MARK} I am ready!")


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
        await ctx.send(
            embed=to_send,
            allowed_mentions=discord.AllowedMentions().none(),
        )
    except:
        try:
            await ctx.channel.send(
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
        except:
            log.critical(
                traceback.format_exception(
                    type(exception), exception, exception.__traceback__
                )
            )


# if os.environ.get("DISCORD_TESTING") == "1":
#     return os.environ["DISCORD_TEST_GUILDS"].split(",") or None
# else:
#     return None


bot.add_cog(cogs.Meta(bot))
bot.add_cog(cogs.Polling(bot))
bot.add_cog(cogs.CCing(bot))
bot.add_cog(cogs.Misc(bot))
bot.add_cog(background.MetaTasks(bot))
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

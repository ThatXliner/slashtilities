from typing import Dict, Iterable, List

import discord
from discord.ext import commands
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

from slashtilities import log, utils


async def make_numbered_list(stuff: Iterable[str]) -> str:
    output = ""
    for index, item in enumerate(stuff, start=1):
        output += f"{get_emoji_for(index)} " + item + "\n\n"
    return output


async def poll(
    self,
    ctx: commands.Context,
    question: str,
    *choices: str,
    **choices_dict: Dict[str, str],
) -> None:
    log.info("START OF `poll`")
    log.info("Making poll")
    log.debug({question: choices})
    log.info("Poll made; sending response...")
    choices = list(choices)
    choices.extend(choices_dict.values())
    try:
        msg = await ctx.send(
            embed=discord.Embed(
                title=await utils.quote(question),
                description=await make_numbered_list(choices),
                color=discord.Color.blue(),
            )
            .set_author(name=f"{ctx.author} asks:", icon_url=str(ctx.author.avatar_url))
            .set_footer(text=await utils.basically_today("Poll made at {}")),
            allowed_mentions=discord.AllowedMentions().none(),
        )
    except discord.errors.HTTPException:
        log.info("Spam?")
        await ctx.send(
            f"**{ctx.author.mention} asks:**\n" + (await utils.quote(question)),
            allowed_mentions=utils.NO_MENTIONS,
        )
        try:
            msg = await ctx.channel.send(
                embed=discord.Embed(
                    title="Choices:",
                    description=await make_numbered_list(choices),
                    color=discord.Color.blue(),
                ).set_footer(text=await utils.basically_today("Poll made at {}"))
            )
        except discord.errors.HTTPException:
            log.info("yes, it's spam")
            msg = await ctx.channel.send(
                "**Choices:**\n" + (await make_numbered_list(choices)),
                allowed_mentions=discord.AllowedMentions.none(),
            )
    else:
        log.info("Success!")
    try:
        log.info("Trying to add reactions...")
        for emoji in map(get_emoji_for, range(1, len(choices) + 1)):
            await msg.add_reaction(emoji)
    except discord.errors.Forbidden:
        ctx.channel.send(
            embed=(
                await utils.errorize(
                    "I could not add the nessecary reactions to the poll above"
                )
            ).set_footer(text="Gimmei perms now")
        )
    else:
        log.info("Add reactions!")
    log.info("END OF `poll`")


def get_emoji_for(thing: int) -> str:
    log.info(f"Getting emoji {thing}")
    emoji_dict = {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
        10: "🔟",
    }
    log.debug(emoji_dict)
    log.info(f"Got {emoji_dict[thing]}")
    return emoji_dict[thing]


async def yesno(self, ctx: commands.Context, question: str) -> None:
    log.info("START OF `yesno`")
    log.info("Sending response")
    try:
        msg = await ctx.send(
            embed=discord.Embed(
                title=await utils.quote(question),
                description="React with :+1: to agree and with :-1: to disagree.",
                color=discord.Color.blue(),
            )
            .set_author(name=f"{ctx.author} asks:", icon_url=str(ctx.author.avatar_url))
            .set_footer(text=await utils.basically_today("Poll made at {}")),
        )
    except discord.errors.HTTPException:
        log.info("Spam?")
        msg = await ctx.send(
            f"**{ctx.author.mention} asks:**\n" + (await utils.quote(question)),
            allowed_mentions=utils.NO_MENTIONS,
        )
    else:
        log.info("Success!")
    try:
        log.info("Trying to add reactions...")
        await msg.add_reaction("\N{THUMBS UP SIGN}")
        await msg.add_reaction("\N{THUMBS DOWN SIGN}")
    except discord.errors.Forbidden:
        ctx.channel.send(
            embed=(
                await utils.errorize(
                    "I could not add the nessecary reactions to the poll above"
                )
            ).set_footer(text="Gimmei perms now")
        )
    else:
        log.info("Added reactions!")
    log.info("END OF `yesno`")


def create_poll_options(maximum: int) -> List[Dict[str, str]]:
    output = [
        create_option(
            "question",
            "The question that you're asking",
            option_type=SlashCommandOptionType.STRING,
            required=True,
        ),
        create_option(
            "choice1",
            "A choice",
            option_type=SlashCommandOptionType.STRING,
            required=True,
        ),
        create_option(
            "choice2",
            "A choice",
            option_type=SlashCommandOptionType.STRING,
            required=True,
        ),
    ]
    output.extend(
        [
            create_option(
                f"choice{x}",
                "A choice",
                option_type=SlashCommandOptionType.STRING,
                required=False,
            )
            for x in range(3, maximum)
        ]
    )
    return output

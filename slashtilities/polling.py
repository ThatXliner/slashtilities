from typing import Dict, Iterable, List

import discord
from discord.ext import commands
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from slashtilities import utils


async def make_numbered_list(stuff: Iterable[str]) -> str:
    output = ""
    for index, item in enumerate(stuff, start=1):
        output += f"{get_emoji_for(index)} " + item + "\n\n"
    return output


async def poll(ctx: commands.Context, question: str, *choices: str) -> None:
    msg = await ctx.send(
        embed=discord.Embed(
            title=f'"{question}"',
            description=await make_numbered_list(choices),
            color=discord.Color.blue(),
        )
        .set_author(name=f"{ctx.author} asks:", icon_url=str(ctx.author.avatar_url))
        .set_footer(text=await utils.basically_today("Poll made at {}")),
        allowed_mentions=discord.AllowedMentions().none(),
    )
    try:
        for emoji in map(get_emoji_for, range(1, len(choices) + 1)):
            await msg.add_reaction(emoji)
    except discord.errors.Forbidden:
        ctx.channel.send(
            embed=utils.errorize(
                "I could not add the nessecary reactions to the poll above"
            ).set_footer(text="Gimmei perms now")
        )


def get_emoji_for(thing: int) -> str:
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
    return emoji_dict[thing]


async def yesno(ctx: commands.Context, question: str) -> None:
    msg = await ctx.send(
        embed=discord.Embed(
            title="",
            description=await utils.quote(question),
            color=discord.Color.blue(),
        )
        .set_author(name=f"{ctx.author} asks:", icon_url=str(ctx.author.avatar_url))
        .set_footer(text=await utils.basically_today("Poll made at {}")),
    )
    try:
        await msg.add_reaction("\N{THUMBS UP SIGN}")
        await msg.add_reaction("\N{THUMBS DOWN SIGN}")
    except discord.errors.Forbidden:
        ctx.channel.send(
            embed=utils.errorize(
                "I could not add the nessecary reactions to the poll above"
            ).set_footer(text="Gimmei perms now")
        )


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

import discord
from discord.ext import commands
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from slashtilities import utils


async def cc(ctx: commands.Context, *users) -> None:
    await utils.disable(
        ctx,
        "Top.gg requires any bot command that dms arbitrary members to have an opt-out option.\n"
        "I have currently not implemented that for it requires a databse.",
    )
    # await cc_helper(ctx, create_cc_message, "CC", users)


async def cc_helper(ctx: commands.Context, msg_func, atype, users):
    await ctx.defer()
    filtered = [user for user in users if not (user.bot or user.id == ctx.author.id)]
    if filtered:
        last_msg = await utils.get_last_message_from(ctx.author, channel=ctx.channel)
        if last_msg is None:
            ctx.send(embed=utils.errorize(f"Bruh, you have no messages to {atype}"))
        assert last_msg is None
        for user in filtered:
            await (user.dm_channel or await user.create_dm()).send(
                embed=await msg_func(
                    ctx,
                    filtered,
                    from_message=last_msg,
                    to=user,
                )
            )
        await ctx.send(  # XXX: Remove for BCC?
            embed=discord.Embed(
                title=f"I have {atype}'d the following people:",
                description=await make_list(person.mention for person in filtered),
                color=discord.Color.green(),
            ).add_field(
                name=f"Your message I {atype}'d them':",
                value=await utils.quote(last_msg.content)
                + f"\n\n[**Jump to message**]({last_msg.jump_url})",
                inline=False,
            )
        )
    if set(filtered) != set(users):
        if filtered:
            await ctx.channel.send("Wait, someone's missing? Here's why:")
        else:
            await ctx.send(f"You {atype}'d nobody. Here's why:")
        if {user for user in users if not user.bot} == set(filtered):
            await ctx.channel.send(
                ":robot: I can't dm other bots, you know. ~~They actually blocked me :sob:~~"
            )
        elif {user for user in users if not user.id == ctx.author.id} == set(filtered):
            await ctx.channel.send(f":mirror: You can't {atype} yourself-")
        else:  # Both
            await ctx.channel.send(
                ":robot: I can't dm other bots, you know. ~~They actually blocked me :sob:~~"
            )
            await ctx.channel.send(f":mirror: Also, you can't {atype} yourself.")


async def bcc(ctx: commands.Context, *users) -> None:
    await utils.disable(
        ctx,
        "Top.gg requires any bot command that dms arbitrary members to have an opt-out option.\n"
        "I have currently not implemented that for it requires a databse.",
    )
    # await cc_helper(ctx, create_bcc_message, "BCC", users)


async def create_bcc_message(ctx: commands.Context, _, from_message, to):
    return (
        discord.Embed(title="", description="", color=discord.Color.blurple())
        .set_author(
            name=f"You have been BCC'd by {ctx.author}.\n",
            icon_url=ctx.author.avatar_url,
        )
        .add_field(
            name="Message:", value=await utils.quote(from_message.content), inline=False
        )
        .add_field(
            name="Original Message:",
            value=f"[**Jump to message**]({from_message.jump_url})",
            inline=False,
        )
        .set_footer(
            text=await utils.basically_today(
                "This is a BCC (Blind Carbon Copy) made at {}"
            )
        )
    )


async def create_cc_message(ctx: commands.Context, other_people, from_message, to):
    return (
        discord.Embed(title="", description="", color=discord.Color.blurple())
        .set_author(
            name=f"You have been CC'd by {ctx.author}.\n",
            icon_url=ctx.author.avatar_url,
        )
        .add_field(
            name="Message:", value=await utils.quote(from_message.content), inline=False
        )
        .add_field(
            name="Other people who have also been CC'd are:",
            value=await make_list(
                person.mention
                for person in other_people
                if person not in {ctx.author, to}
            ),
            inline=False,
        )
        .add_field(
            name="Original Message:",
            value=f"[**Jump to message**]({from_message.jump_url})",
            inline=False,
        )
        .set_footer(
            text=await utils.basically_today("This is a CC (Carbon Copy) made at {}")
        )
    )


async def make_list(stuff) -> str:
    output = ""
    for item in stuff:
        output += " - " + item + "\n"
    return output


def create_person_options(maximum: int):
    output = [
        create_option(
            "user1",
            "The first person you want to cc",
            option_type=SlashCommandOptionType.USER,
            required=True,
        )
    ]
    output.extend(
        [
            create_option(
                f"user{x}",
                "Another person you want to cc",
                option_type=SlashCommandOptionType.USER,
                required=False,
            )
            for x in range(2, maximum)
        ]
    )
    return output

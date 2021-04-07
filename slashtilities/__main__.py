# TODO: Use embeds
import asyncio
import datetime
import os

import discord
from discord import Color, Embed
from discord_slash import SlashCommand  # Importing the newly installed library.
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option, remove_all_commands

TOKEN = os.environ["DISCORD_TOKEN"]
intents = discord.Intents().default()
client = discord.Client(intents=intents, activity=discord.Game("Listening to summons"))
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    print("\N{WHITE HEAVY CHECK MARK} I am ready!")


def get_testing_guilds():
    if os.environ.get("DISCORD_TESTING") == "1":
        guild_ids = os.environ["DISCORD_TEST_GUILDS"].split(",")
        asyncio.run(slash.sync_all_commands())
        return guild_ids
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
    await ctx.send(
        embed=Embed(
            title=":ping_pong: Pong!",
            description=f"{gotten_ping:.4} ms",
            color=Color.blue(),
        )
    )


@slash.slash(
    name="igotpinged",  # TODO: Add "whopingedme" alias
    description="Get the person who pinged you ever since your last message",
    guild_ids=get_testing_guilds(),
)
async def igotpinged(ctx):
    await ctx.defer()
    try:
        last_msg = await get_last_message_from(ctx.author, channel=ctx.channel)
    except discord.errors.Forbidden:
        await ctx.send(
            embed=Embed(
                title=":x: Error",
                description=(
                    "How do you expect me to find your last message if "
                    "I don't even have access to this channel???"
                ),
                color=Color.red(),
            ).set_footer(text="What an idiot")
        )
    else:
        print("Getting last ping...", end=" ")
        ping_msgs = []
        async for message in ctx.channel.history(
            after=last_msg,
            limit=None,  # or 9000?
        ):
            if ctx.author.mentioned_in(message):
                ping_msgs.append(message)

        if len(ping_msgs) > 0:
            print("\N{WHITE HEAVY CHECK MARK}")
            if len(ping_msgs) > 1:
                to_send = Embed(
                    title=":mag: Found!",
                    description="The following people did:",
                    color=Color.green(),
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
                        Embed(
                            title=":mag: Found!",
                            description=f"{ping_msgs[0].author.mention} pinged you [**here**]({ping_msgs[0].jump_url})",
                            color=Color.green(),
                        )
                    )
                )
        else:
            print("\N{GHOST}")
            await ctx.send(
                embed=Embed(
                    title=":ghost: Not found! D:",
                    description="I didn't find anyone. You probably got ***ghost pinged***",
                    color=Color.red(),
                )
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


@slash.slash(
    name="cc",
    description="CC other people your last message",
    guild_ids=get_testing_guilds(),
    options=create_person_options(10),
)
async def cc(ctx, *users) -> None:
    await cc_helper(ctx, create_cc_message, "CC", users)


async def cc_helper(ctx, msg_func, atype, users):
    await ctx.defer()
    filtered = [user for user in users if not (user.bot or user.id == ctx.author.id)]
    if filtered:
        last_msg = await get_last_message_from(ctx.author, channel=ctx.channel)
        for user in filtered:
            await (user.dm_channel or await user.create_dm()).send(
                embed=await msg_func(
                    ctx,
                    filtered,
                    from_message=last_msg,
                )
            )
        await ctx.send(  # XXX: Remove for BCC?
            embed=Embed(
                title=f"I have {atype}'d the following people:",
                description=await make_list(person.mention for person in filtered),
                color=Color.green(),
            ).add_field(
                name=f"Your message I {atype}'d them':",
                value=await quote(last_msg.content)
                + f"\n\n[**Jump to message**]({last_msg.jump_url})",
                inline=False,
            )
        )
    if set(filtered) != set(users):
        if filtered:
            await ctx.channel.send("Wait, someone's missing? Here's why:")
        else:
            await ctx.send(f"You {atype}'d nobody. Here's why:")
        if {user for user in users if not user.id == ctx.author.id} == set(filtered):
            await ctx.channel.send(
                ":robot: I can't dm other bots, you know. ~~They actually blocked me :sob:~~"
            )
        elif {user for user in users if not user.bot} == set(filtered):
            await ctx.channel.send(f":mirror: You can't {atype} yourself-")
        else:  # Both
            await ctx.channel.send(
                ":robot: I can't dm other bots, you know. ~~They actually blocked me :sob:~~"
            )
            await ctx.channel.send(f":mirror: Also, you can't {atype} yourself.")


@slash.slash(
    name="bcc",
    description="BCC other people your last message",
    guild_ids=get_testing_guilds(),
    options=create_person_options(10),
)
async def bcc(ctx, *users) -> None:
    await cc_helper(ctx, create_bcc_message, "BCC", users)


async def create_bcc_message(ctx, _, from_message):
    return (
        Embed(title="", color=Color.blurple())
        .set_author(
            name=f"You have been BCC'd by {ctx.author}.\n",
            icon_url=ctx.author.avatar_url,
        )
        .add_field(
            name="Message:", value=await quote(from_message.content), inline=False
        )
        .add_field(
            name="Original Message:",
            value=f"[**Jump to message**]({from_message.jump_url})",
            inline=False,
        )
        .set_footer(
            text=datetime.datetime.today().strftime(
                "This is a BCC (Blind Carbon Copy) made at %B, %d, %Y (%m/%d/%Y) %I:%M %p"
            )
        )
    )


async def create_cc_message(ctx, other_people, from_message):
    return (
        Embed(title="", color=Color.blurple())
        .set_author(
            name=f"You have been CC'd by {ctx.author}.\n",
            icon_url=ctx.author.avatar_url,
        )
        .add_field(
            name="Message:", value=await quote(from_message.content), inline=False
        )
        .add_field(
            name="Other people who have also been CC'd are:",
            value=await make_list(
                person.mention for person in other_people if person != ctx.author
            ),
            inline=False,
        )
        .add_field(
            name="Original Message:",
            value=f"[**Jump to message**]({from_message.jump_url})",
            inline=False,
        )
        .set_footer(
            text=datetime.datetime.today().strftime(
                "This is a CC (Carbon Copy) made at %B, %d, %Y (%m/%d/%Y) %I:%M %p"
            )
        )
    )


async def quote(msg: str) -> str:
    output = ""
    for line in msg.splitlines():
        output += "> " + line
    return output


async def make_list(stuff) -> str:
    output = ""
    for item in stuff:
        output += " - " + item + "\n"
    return output


async def make_numbered_list(stuff) -> str:
    output = ""
    for index, item in enumerate(stuff, start=1):
        output += f"{get_emoji_for(index)} " + item + "\n\n"
    return output


def create_poll_options(maximum: int):
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


@slash.slash(
    name="poll",
    description="Send a multi-choice poll (not mutually exclusive)",
    guild_ids=get_testing_guilds(),
    options=create_poll_options(10),
)
async def poll(ctx, question: str, *choices):
    msg = await ctx.send(
        embed=Embed(
            title=f'"{question}"',
            description=await make_numbered_list(choices),
            color=Color.blue(),
        )
        .set_author(name=f"{ctx.author} asks:", icon_url=ctx.author.avatar_url)
        .set_footer(
            text=datetime.datetime.today().strftime(
                "Poll made at %B, %d, %Y (%m/%d/%Y) %I:%M %p"
            )
        ),
        allowed_mentions=discord.AllowedMentions().none(),
    )
    for emoji in map(get_emoji_for, range(1, len(choices) + 1)):
        await msg.add_reaction(emoji)


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


@slash.slash(
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
async def yesno(ctx, question: str):
    msg = await ctx.send(
        embed=Embed(title="", description=await quote(question), color=Color.blue())
        .set_author(name=f"{ctx.author} asks:", icon_url=ctx.author.avatar_url)
        .set_footer(
            text=datetime.datetime.today().strftime(
                "Poll made at %B, %d, %Y (%m/%d/%Y) %I:%M %p"
            )
        )
    )
    await msg.add_reaction("\N{THUMBS UP SIGN}")
    await msg.add_reaction("\N{THUMBS DOWN SIGN}")


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

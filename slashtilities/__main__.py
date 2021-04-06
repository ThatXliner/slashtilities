# TODO: Use embeds
import os

import discord
import discord.ext.commands
from discord_slash import SlashCommand  # Importing the newly installed library.
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option, remove_all_commands_in

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
    await ctx.defer()
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


@slash.slash(  # TODO: Refactor to remove code duplication. This and BCC
    name="cc",
    description="Send a carbon copy of your last message to other people in dms",
    guild_ids=get_testing_guilds(),
    options=create_person_options(10),
)
async def cc(ctx, *users) -> None:
    await ctx.defer()
    filtered = [user for user in users if not (user.bot or user.id == ctx.author.id)]
    if filtered:
        for user in filtered:
            await (user.dm_channel or await user.create_dm()).send(
                await create_cc_message(ctx, filtered)
            )
        await ctx.send(
            "I have CC'd the following people:\n"
            + (
                await make_list(
                    f"`{person.name}#{person.discriminator}`" for person in filtered
                )
            )
        )
    if set(filtered) != set(users):
        if filtered:
            await ctx.channel.send("Wait, someone's missing? Here's why:")
        else:
            await ctx.send("You CC'd nobody. Here's why:")
        if {user for user in users if user.bot} == set(filtered):
            await ctx.channel.send(
                ":robot: I can't dm other bots, you know. ~~They actually blocked me :sob:~~"
            )
        elif {user for user in users if user.id == ctx.author.id} == set(filtered):
            await ctx.channel.send(":mirror: You can't send a cc to yourself-")
        else:  # Both
            await ctx.channel.send(
                ":robot: I can't dm other bots, you know. ~~They actually blocked me :sob:~~"
            )
            await ctx.channel.send(":mirror: Also, you can't send a cc to yourself.")


@slash.slash(
    name="bcc",
    description="Send a blind carbon copy of your last message to other people in dms",
    guild_ids=get_testing_guilds(),
    options=create_person_options(10),
)
async def bcc(ctx, *users) -> None:
    await ctx.defer()
    filtered = [user for user in users if not (user.bot or user.id == ctx.author.id)]
    if filtered:
        for user in filtered:
            await (user.dm_channel or await user.create_dm()).send(
                await create_bcc_message(ctx)
            )
        await ctx.send(
            "I have BCC'd the following people:\n"
            + (await make_list(f"`{person}`" for person in filtered))
        )
    if set(filtered) != set(users):
        if filtered:
            await ctx.channel.send("Wait, someone's missing? Here's why:")
        else:
            await ctx.send("You BCC'd nobody. Here's why:")
        if {user for user in users if user.bot} == set(filtered):
            await ctx.channel.send(
                ":robot: I can't dm other bots, you know. ~~They actually blocked me :sob:~~"
            )
        elif {user for user in users if user.id == ctx.author.id} == set(filtered):
            await ctx.channel.send(":mirror: You can't send a bcc to yourself-")
        else:  # Both
            await ctx.channel.send(
                ":robot: I can't dm other bots, you know. ~~They actually blocked me :sob:~~"
            )
            await ctx.channel.send(":mirror: Also, you can't send a bcc to yourself.")


async def create_bcc_message(ctx):
    from_message = await get_last_message_from(ctx.author, channel=ctx.channel)
    return (
        f"You have been BCC'd by {ctx.author.mention}.\n"
        + "Message:\n"
        + (await quote(from_message.content))
        + f"\n*Here: {from_message.jump_url}*\n"
        + "\nThis is a BCC (Blind Carbon Copy)"
        + "\n"
    )


async def create_cc_message(ctx, other_people):
    from_message = await get_last_message_from(ctx.author, channel=ctx.channel)
    return (
        f"You have been CC'd by {ctx.author.mention}.\n"
        + "Message:\n"
        + (await quote(from_message.content))
        + f"\n*Here: {from_message.jump_url}*\n"
        + "\nOther people who have also been CC'd are:\n"
        + (await make_list(person.mention for person in other_people))
        + "\n"
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
    description="Send a multi-choice poll. (Mutually exclusive options not supported)",
    guild_ids=get_testing_guilds(),
    options=create_poll_options(10),
)
async def poll(ctx, question: str, *choices):
    msg = await ctx.send(
        f"{ctx.author.mention} asks:\n\n> {question}\n\n"
        + await make_numbered_list(choices),
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
    description="Send a yes or no question (Mutually exclusive options not supported)",
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
    msg = await ctx.send(f"{ctx.author.mention} asks:\n> {question}")
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

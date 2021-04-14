import discord
from slashtilities import log


async def invite(ctx):
    log.info("Sending invite links...")
    await ctx.send(
        embed=discord.Embed(
            title="Invite links",
            description="Here are some invite links you can use to invite the bot",
            color=discord.Color.green(),
        )
        .add_field(
            name="Top.gg", value="[**Link**](https://top.gg/bot/828341132865437737)"
        )
        .add_field(
            name="Discord Bot List",
            value="[**Link**](https://discordbotlist.com/bots/slashtilities)",
        )
        .add_field(
            name="Direct invite link",
            value="[**Link**](http://thatxliner.github.io/discord/bots/slashtilities.html)",
        )
        .set_footer(text="You are an epic person :)")
    )
    log.info("Done!")
    log.info("END OF `invite`")


async def vote(ctx):
    log.info("Sending vote links...")
    await ctx.send(
        embed=discord.Embed(
            title="Vote links",
            description="Want to help support us and show your thankfulness? Just vote for our bot!",
            color=discord.Color.green(),
        )
        .add_field(
            name="Top.gg",
            value="[**Vote here!**](https://top.gg/bot/828341132865437737/vote)",
        )
        .add_field(
            name="Discord Bot List",
            value="[**Upvote Here!**](https://discordbotlist.com/bots/slashtilities/upvote)",
        )
        .add_field(
            name="GitHub",
            value="[**Star Here!**](https://github.com/ThatXliner/slashtilities)",
        )
        .set_footer(text="You are an epic person :)")
    )
    log.info("Done!")
    log.info("END OF `vote`")

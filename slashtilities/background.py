from discord.ext import tasks
from discord.ext import commands
import discord
from slashtilities import log

# pylint: disable=E1101  # Man, get your types right


class MetaTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.change_status.start()

    def cog_unload(self):
        self.change_status.cancel()

    @tasks.loop(minutes=30)
    async def change_status(self):
        amount = len(self.bot.guilds)
        log.info(f"I saw {amount} of servers")
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{amount} servers",
            )
        )

    @change_status.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()

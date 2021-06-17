import asyncpg
import discord
from discord.ext import commands
from slashtilities import db, utils
from discord_slash import cog_ext
from discord_slash.utils import manage_commands
from discord_slash.model import SlashCommandOptionType


class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.SETTING_NAMES = {"dm", "should_dm"}

    @cog_ext.cog_subcommand(
        base="settings", name="show", description="Show your settings"
    )
    async def slash_show(self, ctx) -> None:
        await self.settings_show(ctx)

    @cog_ext.cog_subcommand(
        base="settings",
        name="set",
        description="Set your settings",
        options=[
            manage_commands.create_option(
                "value",
                "The name of the value to change",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
            manage_commands.create_option(
                "to",
                "The value to change to",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
        ],
    )
    async def slash_set(self, ctx, setting_name: str, to: str) -> None:
        await self.settings_set(ctx, setting_name, to)

    @commands.group(name="settings")
    async def normal_settings(self, ctx) -> None:
        """Do stuff with your settings"""
        if ctx.invoked_subcommand is None:
            await self.settings_show(ctx)

    @normal_settings.command("show")
    async def normal_show(self, ctx) -> None:
        """Show your settings"""
        await self.settings_show(ctx)

    @normal_settings.command("set")
    async def normal_set(self, ctx, setting_name: str, to: str) -> None:
        """Set your settings"""
        await self.settings_set(ctx, setting_name, to)

    async def settings_show(self, ctx) -> None:
        to_send = discord.Embed(
            title="Your settings",
            description="Fresh from the database! :bread:",
            color=discord.Color.blurple(),
        )
        for name, value in (await db.get_preferences_for(ctx.author.id)).items():
            if name == "snowflake":
                continue
            to_send.add_field(name=name, value=value)
        await ctx.send(embed=to_send)

    async def settings_set(self, ctx, setting_name: str, to: str) -> None:
        setting_name = setting_name.lower()
        if setting_name not in self.SETTING_NAMES:
            await ctx.send(embed=await utils.errorize("Setting not found"))
        else:
            try:
                converted = await utils.convert(to)
            except ValueError:
                await ctx.send(embed=await utils.errorize(f"{to} is an invalid value"))
            else:
                try:
                    await db.update_preferences_for(ctx.author.id, converted)
                except asyncpg.exceptions.DataError:
                    await ctx.send(
                        embed=await utils.errorize(
                            f"{to} is an invalid value for {setting_name}"
                        )
                    )
                else:
                    await ctx.send(
                        embed=await utils.success(
                            f"The setting `{setting_name}` is now `{converted}`"
                        )
                    )

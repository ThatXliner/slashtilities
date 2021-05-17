import importlib

from discord.ext import commands
from discord.ext.commands import Cog as _Cog
from discord_slash import cog_ext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

from slashtilities import ccing, polling


class CogMeta(type):
    def __new__(cls, name, bases, attrs):
        module = importlib.import_module(f".{name.lower()}", "slashtilities")

        def init(self, bot: commands.Bot) -> None:
            self.bot = bot

        new_attrs = attrs.copy()
        for func_name, options in attrs.items():
            if not func_name[0] == "_":
                base_func = getattr(module, func_name)
                assert base_func.__name__ == func_name
                if isinstance(options, str):
                    options = {"description": options}
                new_attrs[f"slash_{func_name}"] = cog_ext.cog_slash(
                    **{"name": func_name, "description": base_func.__doc__, **options}
                )(base_func)
                print(f"{name}.{func_name}")
                new_attrs[func_name] = commands.command(name=func_name)(base_func)

        new_attrs["__init__"] = init
        new_class = type(name, bases + (_Cog,), new_attrs)

        return new_class


# def cogged(cls):
#     module = importlib.import_module(cls.__name__.lower(), "slashtilities")
#
#     def init(self, bot: Bot) -> None:
#         self.bot = bot
#
#     class new_class(cls, Cog):
#         ...
#
#     for func_name, options in new_class.__dict__.items():
#         if not func_name[0] == "_":
#             base_func = getattr(module, func_name)
#             setattr(
#                 new_class,
#                 f"slash_{func_name}",
#                 cog_ext.cog_slash(name=func_name, **options)(base_func),
#             )
#             setattr(
#                 new_class,
#                 func_name,
#                 base_func,
#             )
#
#     setattr(new_class, "__init__", init)
#     return new_class


# @cogged
class Meta(metaclass=CogMeta):
    invite = "Our bot's invite links!"
    vote = "Vote for our bot here!"


class Polling(metaclass=CogMeta):
    yesno = {
        "description": "Send a yes-or-no question (not mutually exclusive)",
        "options": [
            create_option(
                "question",
                "The question you're going to ask",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
        ],
    }
    poll = {
        "description": "Send a multi-choice poll (not mutually exclusive)",
        "options": polling.create_poll_options(10),
    }


class CCing(metaclass=CogMeta):
    cc = {
        "description": "CC other people your last message",
        "options": ccing.create_person_options(10),
    }
    bcc = {
        "description": "BCC other people your last message",
        "options": ccing.create_person_options(10),
    }


# class Meta(Cog):
#     @cog_ext.cog_slash(name="vote", description="Vote for our bot here!")
#     async def slash_invite(self, ctx, *args, **kwargs) -> None:
#         await meta.invite(ctx, *args, **kwargs)
#
#     async def invite(self, ctx, *args, **kwargs) -> None:
#         await meta.invite(ctx, *args, **kwargs)

# Slashtilities
<center>

<img src="./assets/banner.png" height="100"></img>

***A nice and simple, [slash command](https://discord.com/developers/docs/interactions/slash-commands#slash-commands)-based, [Discord](https://discord.com/) utility bot.***

</center>
## Features

 - Intuitive, [slash command](https://discord.com/developers/docs/interactions/slash-commands#slash-commands)-based interface
 - Open source and written in [discord.py](https://discordpy.readthedocs.io/) and [discord-py-slash-command](https://discord-py-slash-command.readthedocs.io)

## Instructions

### Adding to your server

Just follow [this link](https://thatxliner.github.io/discord/bots/slashtilities.html) and add it to your server like any other bot.

### Self-hosting the bot

First, clone this git repository

```bash
$ git clone https://github.com/ThatXliner/slashtilities
```

Second, install the requirements (requires [Poetry](https://python-poetry.org))

```bash
$ poetry install
```

Finally, start running the bot. Remember to replace `<your token here>` with your actual Discord bot token.

```bash
$ DISCORD_TOKEN="<your token here>" poetry run python -m slashtilities
```

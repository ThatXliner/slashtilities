# Slashtilities
<center>

<img src="./assets/banner.png" height="100"></img>

***A nice and simple, [slash command](https://discord.com/developers/docs/interactions/slash-commands#slash-commands)-based, [Discord](https://discord.com/) utility bot.***

</center>

## Features

 - Intuitive, [slash command](https://discord.com/developers/docs/interactions/slash-commands#slash-commands)-based interface
 - Open source and written in [discord.py](https://discordpy.readthedocs.io/) and [discord-py-slash-command](https://discord-py-slash-command.readthedocs.io)
 - All commands do not require a database (for now)
 - Zero configuration needed

### Available commands

#### `/ping`

> Returns the bot's [ping](https://www.rtr.at/TKP/service/rtr-nettest/help/test_result/netztestfaq_testergebnis_0300.en.html) in miliseconds

Other than being a basic sanity check, this command is quite useless.

#### `/igotpinged`

> Get the last message pinging you after your latest message sent in the channel

When you're in servers where people talk 100 messages a minute, this command is useful when

1. You got pinged when you come back
2. You don't want to scroll through all those messages to find who pinged you and why

While Discord's find feature is nice, typing `/igotpinged` saves a lot of keystrokes or (in the case of mobile) tapping.

#### `/???`

> ???

Suggest your command in our [issue tracker](https://github.com/ThatXliner/slashtilities/issues/)! Maybe the newest command came from your idea!

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

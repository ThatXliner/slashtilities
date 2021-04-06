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

> Get the last message pinging you after your last message sent in the channel

When you're in servers where people talk 100 messages a minute, this command is useful when

1. You got pinged when you come back
2. You don't want to scroll through all those messages to find who pinged you and why

While Discord's find feature is nice, typing `/igotpinged` saves a lot of keystrokes or (in the case of mobile) tapping.

#### `/cc @someone, ...`

> Sends a dm to the people you `/cc`'d with your last message's contents and jump-link. Also tells them who else you CC'd

Because just pinging them is risky.

1. Your original message (or the message you used to ping them) can get deleted
2. And if number 1 happens, your reputation will be ruined because you "ghost pinged them"

DMs are a safe and persistent place for dumping messages.

**NOTE:** Because of Discord's current API limits, you can only [`/cc`](#cc-someone-)/[`/bcc`](#bcc-someone-) a limited number of people. I have currently made that limit *10* but **if you want to make the limit higher, request it in our [issue tracker][issue]**

#### `/bcc @someone, ...`

> Sends a dm to the people you `/bcc`'d with your last message's contents and jump-link

Basically [`/cc`](#cc-someone-) but the dm message doesn't tell them who else you've CC'd.

#### `/poll question, choice1, choice2, ...`

> Ask a multi-choice poll (not mutually exclusive)

This is useful if you want a group vote. This command will also add the nessecary reactions.

**NOTE:** The current limit of choices is 10

#### `/yesno question`

> Ask a yes-or-no question

Because yes. Or was it no?

#### `/???`

> ???

Suggest your command in our [issue tracker][issue]! Maybe the newest command came from your idea!

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

[issue]: https://github.com/ThatXliner/slashtilities/issues/

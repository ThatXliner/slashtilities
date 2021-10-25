# Slashtilities
<center>

<img src="./assets/banner.png" height="100"></img>

***A nice and simple, [slash command](https://discord.com/developers/docs/interactions/slash-commands#slash-commands)-based, [Discord](https://discord.com/) utility bot.***

</center>

## Features

 - Intuitive, [slash command](https://discord.com/developers/docs/interactions/slash-commands#slash-commands)-based interface
 - Open source and written in [discord.py](https://discordpy.readthedocs.io/) and [discord-py-slash-command](https://discord-py-slash-command.readthedocs.io)

### Available commands
#### `/ping`

> Returns the bot's [ping](https://www.rtr.at/TKP/service/rtr-nettest/help/test_result/netztestfaq_testergebnis_0300.en.html) in miliseconds

Other than being a basic sanity check, this command is quite useless.

#### `/igotpinged`

> Get the last message(s) pinging you after your last message sent in the channel

When you're in servers where people talk 100 messages a minute, this command is useful when

1. You got pinged when you come back
2. You don't want to scroll through all those messages to find who pinged you and why

While Discord's find feature is nice, typing `/igotpinged` saves a lot of keystrokes or (in the case of mobile) tapping.

#### `/emoji_backup`

> Back up the guild's emojis

Get a copy of the current guild (server)'s emojis. This is useful for backing up emojis for a guild that freely allows emoji modification (e.g. [my server](https://thatxliner.github.io/discord/server.html)).

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

> Send a multi-choice poll (options mutually exclusive)

This is useful if you want a group vote. This command will also add the nessecary reactions.

**NOTE:** The current limit of choices is 9

![demo](./multichoicepoll.png)

#### `/yesno question`

> Send a yes-or-no question (options mutually exclusive)

Because yes. Or was it no?

#### `/invite`

> Our bot's invite links!

Because yes!

#### `/vote`

> Vote for our bot here!

Please.

#### `/???`

> ???

Suggest your command in our [issue tracker][issue]! Maybe the newest command came from your idea!

[issue]: https://github.com/ThatXliner/slashtilities/issues

## Instructions

### Adding to your server

Just follow [this link](https://thatxliner.github.io/discord/bots/slashtilities.html) and add it to your server like any other bot.

### Self-hosting the bot

If you have Python 3.7+ installed (instructions [here](#python-37-and-pip)), you may run our experimental auto-installer via

```bash
$ curl -sSf https://raw.githubusercontent.com/ThatXliner/slashtilities/master/autoselfhost.py | python3 -
```

Or you can [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/ThatXliner/slashtilities) (you may need to add the [PostgreSQL Add-on](https://elements.heroku.com/addons/heroku-postgresql) in order for it to work properly)

#### Requirements

 - Python 3.7+ and pip OR the latest stable version of Poetry
 - PostgreSQL
 - Git (of course)

If you're missing any of these requirements, check the [install requirements instructions](#installing-requirements)

#### First steps

No matter what, you still need to clone this git repository

```bash
$ git clone https://github.com/ThatXliner/slashtilities
```

#### Installing dependancies

You got 2 options: [install the dependancies with poetry](#with-poetry) or [install the dependancies with pip (in a venv, of course)](#with-python-and-pip)

##### With Python and pip

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
(venv) $ pip install -r requirements.txt
```

##### With Poetry

```bash
$ poetry install
```

#### Running the bot

Finally, start running the bot. Remember to replace `<your token here>` with your actual Discord bot token.

You still got 2 options: [run the bot with poetry](#run-with-poetry) or [run the bot with Python in a venv](#run-with-python)


##### Run with Poetry

```bash
$ DISCORD_TOKEN="<your token here>" poetry run python -m slashtilities
```

##### Run with Python

```bash
$ source .venv/bin/activate
(venv) $ DISCORD_TOKEN="<your token here>" python3 -m slashtilities
```

### Installing requirements

#### Git

You should have Git. To check, run

```bash
$ git --help
```

If you don't, how come you're browsing GitHub? Anyways, you can download Git [here](https://git-scm.com/downloads)

#### Python 3.7+ and pip

You might already have Python 3.7+. To check, run

```bash
$ python3 -V
```

Get the latest version of Python [here](https://www.python.org/downloads/). Once you did that run

```bash
$ python3 -m ensurepip --upgrade --user
```

#### Poetry (optional)

To make life easier, you can install Poetry [here](https://python-poetry.org/docs/#installation) or with

```bash
$ python3 -m pip install poetry
```

#### PostgreSQL

You need PostgreSQL if you want features that have settings (e.g. `cc` and `bcc`).

If you don't want to install PostgreSQL, set the environment variable `NO_DB` to `1` when running the bot.

Otherwise, download PostgreSQL from [here](https://www.postgresql.org/download/)

Verify that your PostgreSQL is installed via

```bash
$ psql -l
```

It should not error

### Self-host (uninstalling)

Just remove the `slashtilities` directory

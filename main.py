# -*- coding: utf-8 -*-

from Source.Client.bot import Bot

import json


def main() -> None:
    """
    Runs the start function for the discord bot

    :return:
   """

    # Read config file
    with open("./Config/settings.json", "r") as f:
        config = json.loads(f.read())

    # Create bot instance
    bot = Bot(config)

    # Run bot
    bot.run(config['discord']['token'])


if __name__ == "__main__":
    main()
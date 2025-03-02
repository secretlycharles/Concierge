# -*- coding: utf-8 -*-

# Important Discord Libraries
import hikari
import lightbulb

# Needed Libraries
import logging
import asyncio
import json
import time
import os

# Setup Logger
logger = logging.getLogger("hikari")
logger.setLevel(logging.INFO)

# Get config file
with open("./Settings/config.json", "r") as file:
    config = json.loads(file.read())

# Create a GatewayBot instance
bot = hikari.GatewayBot(
    token=config["discord"]["token"],
    intents=hikari.Intents.ALL,
)
client = lightbulb.client_from_app(bot)

# Ensure client starts once the bot is run
bot.subscribe(hikari.StartingEvent, client.start)

@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    """
    An on_starting event that fires when the bot starts up, also loads extensions

    :param _: hikari.StartingEvent
    :return:
    """
    # Load any extensions within the 'Extensions' folder, we can also make this recursive for folder structure
    extensions = []
    for file in os.listdir("Source/Extensions"):
        # Filter out nothing that's .py and ignore __init__.py or others
        if not file.endswith(".py") or file.startswith("_"):
            continue
        extensions.append("Source.Extensions." + file.replace(".py", ""))
    logging.info(f"Loading all found extensions! Extensions: {extensions}")

    # Load extensions
    await client.load_extensions(*extensions)
    logging.info("All extensions loaded!")

    # Start the bot - make sure commands are synced properly
    await client.start()


@bot.listen(hikari.StartedEvent)
async def on_started(_: hikari.StartedEvent) -> None:
    """
    An on_started event that fires when the bot is ready/starts

    :param _: hikari.StartedEvent
    :return: None
    """
    logging.info(f"'{bot.get_me().username}' has connected to Discord!")


@bot.listen(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
    """
    Listens into guilds' channel messages until a 'trigger word' is said
    and executes an explicit copypasta defined in 'config.json'

    :param event: hikari.GuildMessageCreateEvent
    :return: None
    """
    # Only execute if user is human
    if not event.is_human:
        return

    # Handle a reply
    msg = event.content.lower()

    # Execute only if there's a trigger word
    trigger_word = next((trigger for trigger in config["llm"]["triggers"] if trigger in msg), None)
    if trigger_word is None:
        return
    logging.info(f"{event.get_guild().name}/{event.get_channel()} a trigger word was detected! Detected Word: '{trigger_word}'")

    # Handle a reply
    copypasta = config["copypasta"].get(trigger_word, None)
    if copypasta is None:
        logging.error(f"A copypasta was detected! But no reply was set for it, Detected Word: '{trigger_word}'")
        return

    # Reply with copypasta
    reply = ' '.join(copypasta)
    await event.message.respond(reply)

def run() -> None:
    """
    Launcher function that runs the bot.

    :return: None
    """
    # Depending on the arch, we can use a better event loop for linux based systems
    if os.name != "nt":
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # Setup logger
    file_handler = logging.FileHandler(f"./Logs/bot_{int(time.time())}.log", encoding="utf-8")  # Specify log filename
    file_handler.setLevel(logging.DEBUG)  # Set file logging level

    # Create a logging format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Run bot
    bot.run(
        activity=hikari.Activity(
            name=f"LLM Bot | Version 0.0.1",
            type=hikari.ActivityType.WATCHING,
        )
    )


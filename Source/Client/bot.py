# -*- coding: utf-8 -*-

# Important Discord Libraries
from discord.app_commands import errors
from discord.ext import commands
from discord import Message
import discord

# Needed libraries
import platform
import logging
import os

# Setup base intents
intents = discord.Intents.all()
intents.message_content = True

class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)

logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())

# File handler
file_handler = logging.FileHandler(filename="./Logs/discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

class Bot(commands.Bot):
    def __init__(self, config: dict):
        super().__init__(
            intents=intents,
            command_prefix=""
        )

        # Bot's file based logger
        self.logger = logger

        # Get config
        self.config = config

    async def setup_hook(self) -> None:
        """
        Prints some information about the bot when it starts, loads cogs and setups error handler.

        :return: None
        """
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(
            f"Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        self.logger.info("-------------------")

        # Load cogs
        await self.load_cogs()

        # Setup tree error handler
        self.tree.error(self.on_app_command_error)

        # Sync tree commands
        await self.tree.sync()

    async def load_cogs(self) -> None:
        """
        The code in this function is executed whenever the bot will start.

        :return: None
        """
        for file in os.listdir(f"./Source/Cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"Source.Cogs.{extension}")
                    self.logger.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(
                        f"Failed to load extension {extension}\n{exception}"
                    )

    async def on_ready(self) -> None:
        """
        Prints when the bot is ready.

        :return:
        """
        self.logger.info(f"'{self.user.name}' has connected to Discord!")

    async def on_app_command_error(self, interaction: discord.Interaction, exception: errors.AppCommandError, /) -> None:
        """
        Handles errors that occur during the execution of an application command.

        :param interaction: discord.Interaction
        :param exception: errors.AppCommandError
        :return: None
        """
        self.logger.error(f"Error while executing command '{interaction.command.name}': {exception}")

        """
        TODO: Add a more robust error handling system that will log errors and return the correct error message to the
        user. For example, if it's a permissions error, it should return a message saying that the user doesn't have the
        correct permissions.
        
        An example:
            if isinstance(exception, errors.CheckFailure):
                embed.title = "You do not meet the requirements to use this command."
                embed.description = "Ensure you have the necessary roles to perform this action. If you believe this is a mistake, please reach out to our support team for assistance."
            elif isinstance(exception, errors.CommandInvokeError):
                embed.title = "An error occurred while executing this command."
                embed.description = "Please contact our support team for assistance. Provide any details about what you were trying to do."
            elif isinstance(exception, errors.MissingPermissions):
                embed.title = "An error occurred while executing this command."
                embed.description = "You are not allowed to execute this command."
            else:
                embed.title = "An unexpected error occurred. Please try again later."
                embed.description = "Please contact our support team for assistance. Provide any details about what you were trying to do."
                
        In theory this entire if statement should work, well I use it for production on my businesses but it's missing a lot more checks
        then it should in reality. I'll be adding more checks as I find more errors but this should be fine for now.
        - charles
        """

        # Return error
        send_method = interaction.followup.send if interaction.response.is_done() else interaction.response.send_message
        await send_method(content="An error has occurred, please contact our devs for further", ephemeral=True)

    async def on_interaction(self, interaction: discord.Interaction) -> None:
        """
        Logs all interactions executed by users.

        :param interaction: discord.Interaction
        :return: None
        """
        if interaction.command:
            self.logger.info(
                f"Interaction Executed! Command: '/{interaction.command.name}' by '{interaction.user}' in '#{interaction.channel}/{interaction.channel_id}'"
            )


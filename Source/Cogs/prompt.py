# -*- coding: utf-8 -*-

# Bot/LLM libraries
from ollama import AsyncClient
from Source.Client.bot import Bot
from discord.ext import commands

# Needed libraries
import discord
import random
import re

class PromptCommand(commands.Cog):
    def __init__(self, bot):
        # Bot object
        self.bot = bot

        # Get config
        self.config = self.bot.config

        # Assign error handler
        self.error_handler = self.bot.on_app_command_error

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Prompt command loaded")

    @discord.app_commands.command(name="prompt", description="Talk to the bot")
    async def prompt(self, interaction: discord.Interaction, message: str) -> None:
        """

        :param interaction: discord.Interaction
        :param message: str
        :return: None
        """
        # Defer response
        await interaction.response.defer(ephemeral=False)

        # Print prompt
        self.bot.logger.info(f"{interaction.user.name}/{interaction.user.id} has prompted the bot for '{message}'")

        # Will choose a randomly model from config file (make sure they are actually downloaded 💀)
        model = random.choice(self.config['llm']['models'])

        # Get a response from llm model (only ollama for rn)
        response = await AsyncClient().chat(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': '\n'.join(self.config['llm']['pre_prompt']) + f"\n\nUser Said: {message}"
                }
            ]
        )

        # Log the model
        self.bot.logger.info(f"{interaction.user.name}/{interaction.user.id} ollama response replied with: {response.message.content}")
        self.bot.logger.debug(response)  # debug log the entire response

        # Reply to user with a specific way depending on the model
        if "deepseek" in model:
            await interaction.followup.send(response['message']['content'].split("</think>")[1])
        else:
            await interaction.followup.send(response['message']['content'])


async def setup(bot: Bot):
    await bot.add_cog(PromptCommand(bot=bot))
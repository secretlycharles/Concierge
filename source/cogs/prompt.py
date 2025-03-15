# -*- coding: utf-8 -*-

# Bot/LLM libraries
from source.utilities.context_manager import ContextManager
from source.client.bot import Bot
from discord.ext import commands
from ollama import AsyncClient

# Needed libraries
import discord
import random


class PromptCommand(commands.Cog):
    def __init__(self, bot):
        # Bot object
        self.bot = bot

        # Context handler
        self.context_handler = ContextManager()

        # Get config
        self.config = self.bot.config

        # Assign error handler
        self.error_handler = self.bot.on_app_command_error

        # Persistent Ollama Client
        self.ollama_client = AsyncClient()

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

        # Retrieve model from config file
        model = self.config['llm']['model']

        # Return an error message if no model was set
        if model == "":
            return await interaction.followup.send(
                "An error has occurred, No model was set!! How am I suppose to talk :rage:"
            )

        # Get a response from llm model
        response = await self.ollama_client.chat(
            model=model,
            messages=[
                {
                    'role': 'system',  # For setting LLM restraints this is the best way.
                    'content': '\n'.join(self.config['llm']['pre_prompt'])
                },
                {
                    'role': 'user',
                    'content': f"\n\nUser Said: {message}"
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
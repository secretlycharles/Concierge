# -*- coding: utf-8 -*-

# Bot/LLM libraries
from typing import Mapping
from source.utilities.ollama_client import OllamaClient
from source.client.bot import Bot
from discord.ext import commands

# Needed libraries
import discord


class PromptCommand(commands.Cog):
    def __init__(self, bot):
        # Bot object
        self.bot = bot

        # Get config
        self.config = self.bot.config

        # Assign error handler
        self.error_handler = self.bot.on_app_command_error

        # Persistent Ollama Client
        self.ollama_client = OllamaClient(bot=self.bot, config=self.config)

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
                "An error has occurred, No model was set! Please contact the developers."
            )

        # Prompt llm model for response
        success, response = await self.ollama_client.prompt(
            guild_id=interaction.guild.id, #type: ignore
            user_id=interaction.user.id,
            message=message,
        )

        # Check for failed success
        if not success:
            return await interaction.followup.send(
                "An error has occurred, while trying to interact with our model! Please contact the developers."
            )

        # Log the model
        self.bot.logger.info(f"{interaction.user.name}/{interaction.user.id} ollama response replied with: {response}")

        # Follow up with a message to the user
        if len(response) <= 2000:
            await interaction.followup.send(response)
        else:
            # Split into chunks of 2000 characters
            chunks = [response[i:i + 2000] for i in range(0, len(response), 2000)]

            # Send the first chunk
            await interaction.followup.send(chunks[0])

            # Send the rest of the chunks
            for chunk in chunks[1:]:
                await interaction.followup.send(chunk)


async def setup(bot: Bot):
    await bot.add_cog(PromptCommand(bot=bot))
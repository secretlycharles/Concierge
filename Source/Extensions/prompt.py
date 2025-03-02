# -*- coding: utf-8 -*-

# LLM libraries
from ollama import AsyncClient

# Needed libraries
import lightbulb
import logging
import random
import json

# Setup logger and loader
logger = logging.getLogger("hikari")
loader = lightbulb.Loader()

@loader.command
class Prompt(
    lightbulb.SlashCommand,
    name="prompt",
    description="Prompt the bot with a message!"
):
    prompt = lightbulb.string("message", "Your prompt to the bot")

    def __init__(self):
        super().__init__()

        # Get config file
        with open("./Settings/config.json", "r") as file:
            self.config = json.loads(file.read())

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        """
        Slash Command to handle /prompt and reply with a message

        :param ctx: lightbulb.Context
        :return: None
        """
        try:
            # We want to defer the response because it's possible the LLM may not respond
            # within the normal interaction window, although it is kinda relatively impossible
            # under normal circumstances but 'users will be users'
            await ctx.defer()

            # Print prompt
            logging.info(f"{ctx.user.username}/{ctx.user.id} has prompted the bot for '{self.prompt}'")

            # Will choose a randomly model from config file (make sure they are actually downloaded 💀)
            model = random.choice(self.config['llm']['models'])

            # Get a response from llm model (only ollama for rn)
            response = await AsyncClient().chat(
                model=model,
                messages=[
                    {
                        'role': 'user',
                        'content': '\n'.join(self.config['llm']['pre_prompt']) + f"\n\nUser Said: {self.prompt}"
                    }
                ]
            )

            # Log the model
            logging.info(f"{ctx.user.username}/{ctx.user.id} ollama response replied with: {response['message']}")
            logging.debug(response)  # debug log the entire response

            # Reply to user
            await ctx.respond(response['message']['content'])
        except Exception as e:
            # This may bug out if the interaction was already replied too, but like, how tf would it error out after the response
            logger.error(f"{ctx.user.username}/{ctx.user.id} failed to process request! Error: {e}")
            await ctx.respond("Beep boop, an error has occurred, pls ask the devs for a fix!!")

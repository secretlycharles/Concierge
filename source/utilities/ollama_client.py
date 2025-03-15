
# Discord/LLM Libs
from source.utilities.context_manager import ContextManager
from source.client.bot import Bot
from ollama import AsyncClient

# Needed libs
from typing import Tuple, List
import json


class OllamaClient:
    def __init__(self, bot: Bot, config: dict):
        # Discord Bot
        self.bot = bot

        # Config file
        self.config = config

        # Get LLM Model
        self.model = self.config["llm"].get("model", None)

        # Ollama Wrapper Client
        self.client = AsyncClient()

        # Context handler
        self.context_handler = ContextManager()

    async def prompt(self, guild_id: int, user_id: int, message: str) -> Tuple[bool, str]:
        """
        Prompt the LLM model
        """
        # Verify we have a model set in the config file
        if self.model is None:
            return False, "An error has occurred, No model was set!! How am I suppose to talk :rage:"

        # Retrieve built prompt
        messages = await self.build_prompt(guild_id, user_id, message)

        # Get a response from llm model
        response = await self.client.chat(
            model=self.model,
            messages=messages
        )

        # Trim response and remove thinking tag
        content = response.message.content.split("</think>")[1]

        # Add context to manger
        self.context_handler.add_context(
            guild_id=guild_id,
            user_id=user_id,
            messages=[
                {
                    'role': 'user',
                    'content': message,
                },
                {
                    'role': 'assistant',
                    'content': content,
                }
            ]
        )

        # Return response
        return True, content


    async def build_prompt(self, guild_id: int, user_id: int, message: str) -> List:
        # Implement context window
        context = self.context_handler.get_context(guild_id=guild_id, user_id=user_id)

        # Base message dict
        messages = [
            {
                'role': 'system',
                'content': '\n'.join(self.config['llm']['pre_prompt'])
            }
        ]

        # Ensure context is correctly inserted (we're returned a list, so we must unpack it into dicts)
        if isinstance(context, list):  # Ensure it is a list
            messages.extend(context)  # Unpack list of context dictionaries

        # Add the user message
        message = {
            'role': 'user',
            'content': message
        }
        messages.append(message)

        print(f"Built prompt: {json.dumps(messages, indent=4)}")

        # Return built prompt
        return messages










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
        self.bot.logger.info(f"LLM Response: {response}")

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
        """
        Build the LLM prompt while attempting to stay below the LLM models' context length
        """
        # Ngl this while true loop can fucking blow up, but honestly since everything is kinda O(1)
        # I can't really see it failing, tokenizer is relatively fast too
        while True:
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

            # Calculate if prompt exceeds token length
            prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
            prompt_tokens = len(self.context_handler.tokenizer.encode(prompt))
            model_context_length = self.context_handler.context_length
            self.bot.logger.info(f"Prompt Tokens: {prompt_tokens}, Model Context Length: {model_context_length}")

            # Check if we have to trim or not
            if prompt_tokens <= self.context_handler.context_length:
                break
            else:
                # Trims the first message in the list until the context length is less than the models' context length
                self.context_handler.trim_user_context(guild_id=guild_id, user_id=user_id)


        # Return built prompt
        return messages









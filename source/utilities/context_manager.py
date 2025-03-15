from typing import Dict, List


class ContextManager:
    def __init__(self, context_length = 131072):
        """
        Initializes a context manager with a nested dictionary structure.

        Dictionary structure:
        {
            guild_id (int): {
                user_id (int): {
                    context_messages (list): [
                        "role" (str): "user" | "assistant",  # Specifies if message is from user or AI
                        "message" (str): "<user message or assistant response>"
                    ]
                }
            }
        }

        - Each `guild_id` maps to a dictionary containing user contexts.
        - Each `user_id` maps to a list of message objects (stored as dictionaries).
        - Each message object contains:
            - `"role"`: Defines whether the message is from the `"user"` or `"assistant"`.
            - `"message"`: The actual text content of the message.
        """
        self.context_dictionary: Dict[int, Dict[int, List]] = {}

        # The amount of tokens a model can handle
        self.context_length: int = context_length

    def add_guild(self, guild_id: int) -> None:
        """
        Ensures that a guild exists in the context dictionary.
        """
        if guild_id not in self.context_dictionary:
            self.context_dictionary[guild_id] = {}

    def add_user(self, guild_id: int, user_id: int) -> None:
        """
        Ensures that a user exists in the specified guild context.
        """
        self.add_guild(guild_id)  # Ensure the guild exists first
        if user_id not in self.context_dictionary[guild_id]:
            self.context_dictionary[guild_id][user_id] = []

    def add_context(self, guild_id: int, user_id: int, messages: List[Dict]) -> None:
        """
        Adds multiple messages to the context of a specific user in a given guild.
        """
        self.add_user(guild_id, user_id) # Ensure the user exists first
        self.context_dictionary[guild_id][user_id].extend(messages)

    def get_context(self, guild_id: int, user_id: int) -> List[Dict]:
        """
        Retrieves the message context for a user in a guild.
        """
        return self.context_dictionary.get(guild_id, {}).get(user_id, [])

    def clear_user_context(self, guild_id: int, user_id: int) -> None:
        """
        Clears the context for a specific user in a guild.
        """
        if guild_id in self.context_dictionary and user_id in self.context_dictionary[guild_id]:
            del self.context_dictionary[guild_id][user_id]

    def clear_guild_context(self, guild_id: int) -> None:
        """
        Clears all contexts within a guild.
        """
        if guild_id in self.context_dictionary:
            del self.context_dictionary[guild_id]

    def clear_all_contexts(self) -> None:
        """
        Clears all stored contexts.
        """
        self.context_dictionary.clear()
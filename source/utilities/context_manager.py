from typing import Dict, List


class ContextManager:
    def __init__(self):
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
        self.context_dictionary: Dict[int, Dict[int, List[str]]] = {}
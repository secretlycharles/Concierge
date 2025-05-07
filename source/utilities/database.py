from typing import Dict, List

import json
import os


class Database:
    def __init__(self, context_manager):
        """
        JSON Based Database System
        """
        # Context Manager
        self.context_manager = context_manager


    def load_db(self):
        """
        Loop through all servers and users in the database
        """
        for guild_id in os.listdir("./database"):
            # Don't load this file, it's not valided
            if "DO_NOT_TOUCH" in guild_id:
                continue

            # Load database
            for user_id in os.listdir(f"./database/{guild_id}"):
                with open(f"./database/{guild_id}/{user_id}", "r") as file:
                    # Clean User_ID so it doesn't have .json
                    guild_id = int(guild_id)
                    user_id = int(user_id.replace(".json", ""))
                    # print(f"Loading user {user_id}")

                    # Add database context to user
                    self.context_manager.add_user(guild_id, user_id)
                    self.context_manager.context_dictionary[guild_id][user_id] = json.load(file)
                    # print(f"Loaded Context: {self.context_manager.context_dictionary[guild_id][user_id]}")

    def write_db(self, guild_id: int, user_id: int, context: List[Dict]) -> None:
        """
        Write or update user messages to JSON Database
        """
        guild_path = f"./database/{guild_id}"
        user_path = f"{guild_path}/{user_id}.json"

        # Make sure guild folder exists
        os.makedirs(guild_path, exist_ok=True)

        # Write entire context to database (too lazy to append :p)
        with open(user_path, "w+") as file:
            file.write(json.dumps(context, indent=4))

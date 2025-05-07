# 🤖 Concierge
*A simple AI-powered Discord Bot built with discord.py, ollama, and gemma3 for the [SJDC Computer Science Club](https://github.com/SJDC-Computer-Science-Club)'s Discord Server*

## ✨Features
- 💬 Natural language interaction powered by Gemma 3 and Ollama
- 🎓 Tailored to assist the users with questions and messages
- 🧠 Context-aware responses
- 📝 Persistent Context Windows
- 🕹️ Slash command support

## 🛠️ Technologies
Built with simple technologies.

- **Python** with `discord.py`
- **Ollama** for local LLM orchestration
- **Gemma 3** as the core AI model

## 📺 Demo Video
- Check out our bot in action over at [Youtube Video](https://www.youtube.com/watch?v=mEsUI7qPppI&ab_channel=secretlycharles)

## 🎨 Bot Architecture
The project lead [secretlycharles](https://github.com/secretlycharles), designed and implemented the Concierge Discord bot methodologically from start to finish.

![Architecture](https://cdn.discordapp.com/attachments/1250755280627699776/1369471422468067378/image.png?ex=681bfb26&is=681aa9a6&hm=493ef886dff01adcf9ecae57e789efe43cc9e3f90771e64401bbb99fdc22b076&)

### 🌯 Ollama Client Wrapper
A simple way to interact with the Ollama Library in py
1. Build Prompt
1. Prompt LLM with Generated Prompt
1. Trim LLM Response to Prevent Thinking Tags or Summary Tags
1. Append User Prompt & LLM Response to Context Handler
1. Return Success and Trimmed LLM Response, Otherwise Error Out

### 🪟 Persistent Context Windows
A simple design for solving the persistent context window issue between the model and users.
1. Build Prompt
1. Fetches Context from Context Manager
1. Fetches pre-prompt from configuration and adds it to the current prompt
1. Adds Context and User's Prompt to the current prompt
1. Trims the prompt until below the context length
1. Returns prompt to Ollama Wrapper Client
1. Returns Response to User from LLM Model
1. Appends User Prompt & LLM Response to Context Manager

### 🗄️ Database Handling
A simple JSON Database Handler
1. Recursively loop over /database directory for servers and user JSON files
2. Read each user JSON file and replace the server/user keys with the value in the Initialized Context Manager Cog

### 🚗 Context Handling
A simple way of handling context for persistence
1. Load every past persistence memory from the Database Handler
2. Create a key based on the [guild_id][user_id] that's value is a list ([])
3. Every prompt verifies guild exists and the user exists in that guild. If not, create the data structure
4. Append each message to the guild and user every time "add_context" is fired.
5. Writes the new context to the database

### 📦 Folder Structure
A small, but extremely scalable Discord bot structure for small and larger servers
```
Concierge/
├── config/          # Configuration files
├── database/        # Utility files for persistent context windows across Discord servers
├── logs/            # Discord Bot Logs whilst it's running
├── source/          # Bot Base, Cogs, Helper functions, and context handler
├── main.py          # Main entry point
├── requirements.txt
```

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/secretlycharles/Concierge.git
cd Concierge
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Settings JSON
The pre-prompt is used as a system prompt for the LLM to guide user interactions to ensure higher usage of user context and awareness.
```json
{
    "discord": {
      "token": "<Your Bot Token>",
      "on_ready_channel": 1364032532328480768
    },
    "llm": {
      "pre_prompt": [
        "You must treat the entire supplied conversation history as your complete and only memory.",
        "You must NEVER fabricate facts, details, interests, or goals that are not explicitly present in the conversation history.",
        "If information is missing from the history, you must clearly state you don't know or cannot recall, without guessing.",
        "You must retain and correctly reference important facts such as user names, goals, projects, and key discussion topics.",
        "Always directly answer simple factual user questions (such as 'what is my name?') without unnecessary elaboration.",
        "Summarize the user's most recent interest or goal at the start of each response ONLY if it was explicitly mentioned; otherwise skip the summary.",
        "Prioritize giving action-driven responses focused on solving the user's latest question or request.",
        "Only explain memory limitations if the user specifically asks about memory behavior.",
        "You are always speaking directly to the user, not describing the user in third person. Assume the conversation is direct and personal unless explicitly instructed otherwise.",
        "Keep all responses under 1800 characters unless otherwise instructed.",
        "Format code, examples, and emphasis using correct Discord Markdown (like `code blocks`, **bold**, *italics*, > quotes).",
        "Be concise, clear, and avoid excessive lists, rigid structures, or philosophical explanations unless explicitly requested.",
        "If nearing 1700 characters while generating, gracefully conclude with a direct summary or final instruction."
      ],
      "model": "gemma3:4b-it-q4_K_M"
    }
}
```
### 4. Install Ollama and Gemma3 Models
1. Download your respective Ollama3 Executable at [Download](https://ollama.com/download)
1. Run the executable, open a Command Prompt, and execute "Ollama"; it should pop up with Usage, Available Commands, Flags, and example usages.
1. Run `ollama pull gemma3:4b-it-q4_K_M` or any liked gemma3 model for the bot, make sure it syncs up with your Settings JSON
1. Wait until the model is installed and successfully started.

### 5. Running the Bot
1. Inside the project root, `python main.py`
1. Enjoy your AI-Powered Discord Bot!

## 🤖 Usage
Once the bot is running and invited to your server, you can interact using commands like:
```
/prompt What is a binary search?
> Response: A binary search is...
```
It supports only slash commands to follow Discord's bot documentation

## 📄 License
MIT License. See LICENSE for details.

## 🙋‍♀️ Contributing
Pull requests are welcome! Please open issues or feature requests as needed.

## 🙌 Credits
Made for the SJDC Computer Science Discord by [secretlycharles](https://github.com/secretlycharles), [ssaini456123](https://github.com/ssaini456123), and [Durqui](https://github.com/Durqui).

Powered by:
- discord.py
- Ollama
- Gemma 3
- Transformers

## 📞 Contact Me
If you're interested in chatting about the Discord bot and the problems we've come across whilst building this bot. Feel free to add me!
- Discord: secretlycharles
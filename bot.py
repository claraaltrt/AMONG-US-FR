import discord
from discord import app_commands
import json
import os
from dotenv import load_dotenv
import os
print("ENVIRONMENT VARIABLES")
print(os.envirion)

# Charger fichier .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN introuvable.")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

bot.run(TOKEN)


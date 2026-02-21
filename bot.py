import os
import discord
from discord import app_commands

intents = discord.Intents.default()
intents.members = True

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()  # Synchronise les slash commands

bot = MyBot()

# ===== READY =====
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

# ===== COMMANDES SLASH =====

@bot.tree.command(name="ping", description="Teste si le bot répond")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong !")

@bot.tree.command(name="hello", description="Le bot te dit bonjour")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Salut {interaction.user.mention} 👋")

@bot.tree.command(name="roll", description="Lance un dé")
async def roll(interaction: discord.Interaction):
    import random
    number = random.randint(1, 6)
    await interaction.response.send_message(f"🎲 Tu as obtenu : {number}")

@bot.tree.command(name="info", description="Infos sur le bot")
async def info(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Nom : {bot.user}\nID : {bot.user.id}"
    )

@bot.tree.command(name="server", description="Infos sur le serveur")
async def server(interaction: discord.Interaction):
    guild = interaction.guild
    await interaction.response.send_message(
        f"Serveur : {guild.name}\n"
        f"Membres : {guild.member_count}\n"
        f"Créé le : {guild.created_at.strftime('%d/%m/%Y')}"
    )

# ===== TOKEN =====
TOKEN = os.environ.get("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN introuvable.")

bot.run(TOKEN)

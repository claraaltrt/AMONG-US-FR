import discord
from discord import app_commands
import json
import os

import os
TOKEN = os.getenv("TOKEN")

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

# ===== FILE POINTS =====
if not os.path.exists("points.json"):
    with open("points.json", "w") as f:
        json.dump({}, f)

def load_points():
    with open("points.json", "r") as f:
        return json.load(f)

def save_points(data):
    with open("points.json", "w") as f:
        json.dump(data, f, indent=4)

# ===== READY =====
@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")

# ===== WELCOME =====
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="général")
    if channel:
        await channel.send(f"Bienvenue {member.mention} 🚀 Clique sur le bouton dans #validation pour accéder au serveur.")

# ===== ANTI LIEN =====
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if "http" in message.content:
        await message.delete()
        await message.channel.send(f"{message.author.mention} 🚫 Les liens sont interdits.")

# ===== VALIDATION BUTTON =====
class ValidationView(discord.ui.View):
    @discord.ui.button(label="Valider", style=discord.ButtonStyle.green)
    async def validate(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name="Membre")
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ Tu as accès au serveur !", ephemeral=True)

@bot.tree.command(name="setup_validation", description="Créer le message de validation")
@app_commands.checks.has_permissions(administrator=True)
async def setup_validation(interaction: discord.Interaction):
    embed = discord.Embed(title="Validation", description="Clique sur le bouton pour accéder au serveur.")
    await interaction.response.send_message(embed=embed, view=ValidationView())

# ===== /game =====
@bot.tree.command(name="game", description="Lancer une game (+1 point)")
async def game(interaction: discord.Interaction):
    data = load_points()
    user = str(interaction.user.id)
    data[user] = data.get(user, 0) + 1
    save_points(data)
    await interaction.response.send_message("🚀 Game lancée ! +1 point")

# ===== /win =====
@bot.tree.command(name="win", description="Donner +5 points à un joueur")
@app_commands.checks.has_permissions(manage_messages=True)
async def win(interaction: discord.Interaction, member: discord.Member):
    data = load_points()
    user = str(member.id)
    data[user] = data.get(user, 0) + 5
    save_points(data)
    await interaction.response.send_message(f"🏆 {member.mention} gagne +5 points !")

# ===== /points =====
@bot.tree.command(name="points", description="Voir tes points")
async def points(interaction: discord.Interaction):
    data = load_points()
    pts = data.get(str(interaction.user.id), 0)
    await interaction.response.send_message(f"🎯 Tu as {pts} points.")

# ===== /leaderboard =====
@bot.tree.command(name="leaderboard", description="Voir le classement")
async def leaderboard(interaction: discord.Interaction):
    data = load_points()
    sorted_users = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]

    msg = "🏆 Classement :\n"
    for user_id, pts in sorted_users:
        member = interaction.guild.get_member(int(user_id))
        if member:
            msg += f"{member.name} : {pts} points\n"

    await interaction.response.send_message(msg)

# ===== VOCAL AUTO =====
@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.name == "Créer un vocal":
        guild = member.guild
        category = after.channel.category

        new_channel = await guild.create_voice_channel(
            name=f"Vocal de {member.name}",
            category=category
        )

        await member.move_to(new_channel)

    if before.channel and before.channel.name.startswith("Vocal de"):
        if len(before.channel.members) == 0:
            await before.channel.delete()

bot.run(TOKEN)
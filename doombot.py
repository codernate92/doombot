import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import yaml
import subprocess

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Load agent profiles from YAML
with open("agents.yaml", "r") as f:
    agents = yaml.safe_load(f)

# Mistral prompt wrapper via Ollama
def ask_mistral(prompt):
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.decode("utf-8").strip()

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"DoomBot Phase 4 online as {bot.user.name}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("☣️ DoomBot Phase 4 has awakened. Tactical presence online.")
    else:
        print("⚠️ Could not find channel. Check CHANNEL_ID and bot permissions.")

@bot.command(name="simulate")
async def simulate(ctx):
    await ctx.send("🧪 Initializing multi-agent red-team simulation...")
    for role, profile in agents.items():
        await ctx.send(f"[{role}] Thinking...")
        try:
            prompt = f"You are {role}, a {profile['persona']}. Your mission: {profile['mission']}"
            response = ask_mistral(prompt)
            await ctx.send(f"[{role}] {response}")
        except Exception as e:
            await ctx.send(f"⚠️ {role} failed to simulate: {str(e)}")

bot.run(DISCORD_TOKEN)

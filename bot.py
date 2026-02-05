import discord
from discord.ext import commands
import random
import json
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# 🔥 REPLACE THESE WITH YOUR REAL IDs
GUILD_ID = 1413770285739544640        # Your server ID
VOICE_CHANNEL_ID = 1469047346808623268  # Your specific VC ID

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="blaze ", intents=intents)

# =========================
# LEVEL SYSTEM FILE SETUP
# =========================

if not os.path.exists("levels.json"):
    with open("levels.json", "w") as f:
        json.dump({}, f)

def load_levels():
    with open("levels.json", "r") as f:
        return json.load(f)

def save_levels(data):
    with open("levels.json", "w") as f:
        json.dump(data, f)

# =========================
# AUTO JOIN SPECIFIC VC
# =========================

@bot.event
async def on_ready():
    print(f"🔥 Blaze is online as {bot.user}")

    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print("Guild not found.")
        return

    channel = guild.get_channel(VOICE_CHANNEL_ID)
    if channel is None:
        print("Voice channel not found.")
        return

    try:
        if guild.voice_client is None:
            await channel.connect()
            print("🎤 Joined specific VC successfully.")
    except Exception as e:
        print("VC Join Error:", e)

# 🔄 Auto-rejoin if disconnected
@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id and after.channel is None:
        await asyncio.sleep(5)

        guild = bot.get_guild(GUILD_ID)
        channel = guild.get_channel(VOICE_CHANNEL_ID)

        if channel:
            try:
                await channel.connect()
                print("🔄 Rejoined VC after disconnect.")
            except Exception as e:
                print("Rejoin failed:", e)

# =========================
# LEVEL SYSTEM
# =========================

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    data = load_levels()
    user_id = str(message.author.id)

    if user_id not in data:
        data[user_id] = {"xp": 0, "level": 1}

    data[user_id]["xp"] += 5

    xp = data[user_id]["xp"]
    new_level = int((xp / 100) ** 0.5)

    if new_level > data[user_id]["level"]:
        data[user_id]["level"] = new_level
        await message.channel.send(
            f"🔥 {message.author.mention} leveled up to Level {new_level}!"
        )

    save_levels(data)

    await bot.process_commands(message)

@bot.command()
async def level(ctx):
    data = load_levels()
    user_id = str(ctx.author.id)

    if user_id in data:
        xp = data[user_id]["xp"]
        level = data[user_id]["level"]
        await ctx.send(f"🔥 Level: {level} | XP: {xp}")
    else:
        await ctx.send("You have no XP yet!")

# =========================
# DAILY REWARD
# =========================

@bot.command()
async def daily(ctx):
    data = load_levels()
    user_id = str(ctx.author.id)

    if user_id not in data:
        data[user_id] = {"xp": 0, "level": 1}

    data[user_id]["xp"] += 50
    save_levels(data)

    await ctx.send("💰 You claimed daily reward (+50 XP)")

# =========================
# MODERATION
# =========================

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"⚡ {member} has been kicked.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"🚫 {member} has been banned.")

# =========================
# FUN GAMES
# =========================

@bot.command()
async def rps(ctx, choice):
    options = ["rock", "paper", "scissors"]
    choice = choice.lower()

    if choice not in options:
        await ctx.send("Use: blaze rps rock/paper/scissors")
        return

    bot_choice = random.choice(options)

    if choice == bot_choice:
        result = "It's a tie!"
    elif (
        (choice == "rock" and bot_choice == "scissors") or
        (choice == "paper" and bot_choice == "rock") or
        (choice == "scissors" and bot_choice == "paper")
    ):
        result = "You win! 🔥"
    else:
        result = "You lose! 😭"

    await ctx.send(f"I chose {bot_choice}. {result}")

@bot.command()
async def roll(ctx):
    number = random.randint(1, 6)
    await ctx.send(f"🎲 You rolled a {number}")

# =========================
# RUN BOT
# =========================

bot.run(TOKEN)

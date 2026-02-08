import discord
from discord.ext import commands
import random
import json
import os
import asyncio
import time
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

GUILD_ID = 1437208326092886099
VOICE_CHANNEL_ID = 1437208326797656199

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="blaze ", intents=intents, help_command=None)

if not os.path.exists("levels.json"):
    with open("levels.json", "w") as f:
        json.dump({}, f)

if not os.path.exists("warnings.json"):
    with open("warnings.json", "w") as f:
        json.dump({}, f)

def load_json(file):
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

@bot.event
async def on_ready():
    print(f"BLAZEPIT Online as {bot.user}")
    guild = bot.get_guild(GUILD_ID)
    if guild:
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel:
            try:
                if guild.voice_client is None:
                    await channel.connect()
            except:
                pass

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id and after.channel is None:
        await asyncio.sleep(5)
        guild = bot.get_guild(GUILD_ID)
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel:
            await channel.connect()

spam_tracker = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id
    current_time = time.time()

    if user_id not in spam_tracker:
        spam_tracker[user_id] = []

    spam_tracker[user_id].append(current_time)
    spam_tracker[user_id] = [
        t for t in spam_tracker[user_id] if current_time - t < 5
    ]

    if len(spam_tracker[user_id]) > 5:
        await message.channel.send(f"{message.author.mention} stop spamming ⚠")
        return

    data = load_json("levels.json")
    uid = str(user_id)

    if uid not in data:
        data[uid] = {"xp": 0, "level": 1, "last_message": 0}

    if current_time - data[uid]["last_message"] > 60:
        data[uid]["xp"] += 5
        data[uid]["last_message"] = current_time

        xp = data[uid]["xp"]
        new_level = int((xp / 100) ** 0.5)

        if new_level > data[uid]["level"]:
            data[uid]["level"] = new_level
            await message.channel.send(
                f"{message.author.mention} leveled up to Level {new_level}!"
            )

        save_json("levels.json", data)

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Only Administrators can use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument.")
    else:
        pass

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="BLAZEPIT Help Panel",
        description="Here’s what I can do:",
        color=discord.Color.orange()
    )

    embed.add_field(
        name="Moderation (Admin Only)",
        value="`blaze kick @user`\n`blaze ban @user`\n`blaze warn @user`\n`blaze mute @user 10`",
        inline=False
    )

    embed.add_field(
        name="Fun Commands",
        value="`blaze rps rock`\n`blaze roll`",
        inline=False
    )

    embed.add_field(
        name="Level System",
        value="`blaze level`\n`blaze daily`",
        inline=False
    )

    embed.add_field(
        name="Voice System",
        value="Auto VC Lock Enabled",
        inline=False
    )

    embed.set_footer(text="BLAZEPIT • Server Core System")
    await ctx.send(embed=embed)

@bot.command()
async def level(ctx):
    data = load_json("levels.json")
    uid = str(ctx.author.id)

    if uid in data:
        await ctx.send(f"Level: {data[uid]['level']} | XP: {data[uid]['xp']}")
    else:
        await ctx.send("No XP yet.")

@bot.command()
async def daily(ctx):
    data = load_json("levels.json")
    uid = str(ctx.author.id)

    if uid not in data:
        data[uid] = {"xp": 0, "level": 1, "last_message": 0}

    data[uid]["xp"] += 50
    save_json("levels.json", data)

    await ctx.send("Daily reward claimed (+50 XP)")

@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await ctx.send(f"{member} kicked.")

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.ban(reason=reason)
    await ctx.send(f"{member} banned.")

@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member, *, reason="No reason"):
    warnings = load_json("warnings.json")
    uid = str(member.id)

    if uid not in warnings:
        warnings[uid] = []

    warnings[uid].append(reason)
    save_json("warnings.json", warnings)

    await ctx.send(f"{member} warned.")

@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, minutes: int):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")

    await member.add_roles(muted_role)
    await ctx.send(f"{member} muted for {minutes} minutes.")

    await asyncio.sleep(minutes * 60)
    await member.remove_roles(muted_role)

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
        result = "You win!"
    else:
        result = "You lose!"

    await ctx.send(f"I chose {bot_choice}. {result}")

@bot.command()
async def roll(ctx):
    await ctx.send(f"You rolled {random.randint(1,6)}")

bot.run(TOKEN)

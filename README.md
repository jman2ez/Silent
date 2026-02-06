# 🔥 BLAZEPIT  
### 🚀 Multipurpose Discord Server Core Bot

> Moderation • Games • Leveling • Voice Lock  
> Built with `discord.py`

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/discord.py-2.x-5865F2?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Stable-success?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-black?style=for-the-badge">
</p>

---

## ⚡ Overview

**BLAZEPIT** is a multipurpose Discord bot designed to act as your server's backbone.

It includes:

- 🛡 Moderation system  
- 🎮 Fun mini games  
- 📊 Automatic leveling system  
- 🎤 Permanent voice channel lock  

---

## 🛡 Moderation Commands

```bash
blaze kick @user
blaze ban @user
```

Permission-based execution required.

---

## 🎮 Fun Commands

```bash
blaze rps rock
blaze roll
blaze daily
blaze level
```

---

## 📊 Level System

- XP gained automatically per message
- Auto level-up detection
- JSON-based storage
- Scalable to database upgrade

### Level Formula

```python
level = int((xp / 100) ** 0.5)
```

---

## 🎤 Voice Channel Lock

**BLAZEPIT:**

- Automatically joins a specific VC on startup
- Rejoins if disconnected
- Designed for 24/7 hosting
- Works on cloud platforms (Koyeb, Railway, VPS)

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/blazepit.git
cd blazepit
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Setup Environment Variable

Create a `.env` file:

```env
DISCORD_TOKEN=your_bot_token_here
```

Or configure it in your hosting provider.

---

### 4️⃣ Configure Server & Voice Channel IDs

Inside `bot.py`:

```python
GUILD_ID = YOUR_SERVER_ID
VOICE_CHANNEL_ID = YOUR_VOICE_CHANNEL_ID
```

Enable Developer Mode in Discord to copy IDs.

---

### 5️⃣ Run Bot

```bash
python bot.py
```

---

## 🔐 Required Bot Permissions

### Enable in Developer Portal:

- MESSAGE CONTENT INTENT
- SERVER MEMBERS INTENT
- PRESENCE INTENT (optional)

### Bot Role Permissions:

- Connect
- Speak
- Kick Members
- Ban Members
- View Channel

---

## 📂 Project Structure

```bash
blazepit/
│
├── bot.py
├── levels.json
├── requirements.txt
└── README.md
```

---

## 🚀 Roadmap

- XP-based role rewards
- Anti-spam system
- Music module
- AI integration
- Slash command support
- Modular cog architecture

---

## 📜 License

MIT License

---

Built with 🔥 by 1STRYKE 

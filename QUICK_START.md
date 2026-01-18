# 🚀 Quick Setup Guide

## Step 1: Copy Environment File
```bash
cp .env.example .env
```

## Step 2: Get Discord Bot Token
1. Go to https://discord.com/developers/applications
2. Create New Application → "Username Sniper"
3. Go to "Bot" → "Add Bot"
4. Click "Copy" under TOKEN

## Step 3: Add Token to .env
Edit `.env` and paste your token:
```
DISCORD_BOT_TOKEN=paste_your_token_here
```

## Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 5: Invite Bot to Server
1. In Developer Portal: OAuth2 → URL Generator
2. Scopes: `bot`
3. Permissions: Send Messages, Embed Links, Attach Files, Read Message History
4. Copy URL → Open in browser → Select server

## Step 6: Run Bot
```bash
python discord_bot.py
```

## Done! 🎉

Use `/snipe` in Discord to start checking usernames!

---

## Pattern Cheat Sheet

| Pattern | Format | Example |
|---------|--------|---------|
| 1 | X_XXX | A_BCD |
| 2 | XX_XX | AB_CD |
| 3 | XXX_X | ABC_D |
| 4 | 1_X2X | 5_A9B |
| 5 | 1X_2X | 5A_9B |
| 6 | 1X2_X | 5A9_B |
| 7 | X1X2X | A5B9C |
| 10 | XX11 | AB12 |
| 11 | 1X1X1X | 5A9B3C |
| 12 | XXX11X | ABC12D |
| 13 | X.X.X | A.B.C |
| 14 | X_X_X | A_B_C |
| 15 | XX1XX | AB5CD |
| Custom | LLDLD | MZ9P5 |

**Custom Pattern Symbols**:
- `L` = Letter (A-Z)
- `l` = lowercase (a-z)
- `D` = Digit (0-9)
- `S` = Symbol (_.-) 
- Other = Keep as-is (.,_-' etc)

## Security Reminder ⚠️

Your `.env` file is in `.gitignore` - it won't be committed to Git.

**NEVER:**
- Share your `.env` file
- Paste token in Discord/chat
- Commit `.env` to repository

**IF COMPROMISED:**
- Delete bot and create new one
- Regenerate token immediately

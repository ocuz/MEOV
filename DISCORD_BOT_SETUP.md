# Discord Bot Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment File
```bash
cp .env.example .env
```

### 3. Get Your Bot Token
- Go to [Discord Developer Portal](https://discord.com/developers/applications)
- Click "New Application"
- Name it "Username Sniper" (or your preferred name)
- Go to "Bot" section and click "Add Bot"
- Under TOKEN, click "Copy"

### 4. Add Token to .env
Edit `.env` and replace:
```
DISCORD_BOT_TOKEN=your_bot_token_here
```
with your actual token:
```
DISCORD_BOT_TOKEN=MzA4NDk3NzA5MDk3MzEyMzI4.DZdxzQ.j...
```

### 5. Invite Bot to Server
- In Developer Portal, go to "OAuth2" → "URL Generator"
- Under "SCOPES", select: `bot`
- Under "PERMISSIONS", select:
  - Send Messages
  - Embed Links
  - Attach Files
  - Read Message History
- Copy the generated URL and open it in your browser
- Select your server and authorize

### 6. Run the Bot
```bash
python discord_bot.py
```

You should see:
```
✅ Bot logged in as Username-Sniper#1234
✅ Synced X command(s)
```

## Usage in Discord

### Commands

#### `/snipe`
Start the username checking process.

**Interactive Flow**:
1. Select a pattern from dropdown
2. Choose quantity (100, 250, 500, or custom)
3. Select platform(s) to check
4. Click "Start Checking"
5. Export results in multiple formats

#### `/help`
Show help and usage instructions.

## Pattern Types

### Built-in Patterns
- **1. X_XXX**: `A_BCD` (Letter_3Letters)
- **2. XX_XX**: `AB_CD` (2Letters_2Letters)
- **3. XXX_X**: `ABC_D` (3Letters_Letter)
- **4. 1_X2X**: `5_A9B` (Digit_Letter+Digit+Letter)
- **5. 1X_2X**: `5A_9B` (Digit+Letter_Digit+Letter)
- **6. 1X2_X**: `5A9_B` (Digit+Letter+Digit_Letter)
- **7. X1X2X**: `A5B9C` (Mixed strict mode)
- **10. XX11**: `AB12` (2Letters+2Digits)
- **11. 1X1X1X**: `5A9B3C` (Alternating Digit+Letter)
- **12. XXX11X**: `ABC12D` (3Letters+2Digits+Letter)
- **13. X.X.X**: `A.B.C` (Dot-separated)
- **14. X_X_X**: `A_B_C` (Underscore-separated)
- **15. XX1XX**: `AB5CD` (2Letters+Digit+2Letters)

### Custom Patterns
Define your own using:
- `L` = Uppercase letter (A-Z)
- `l` = Lowercase letter (a-z)
- `D` = Digit (0-9)
- `S` = Symbol (_.-) 
- Any other character remains literal

**Examples**:
- `LLDLD` → `AB5C9`, `MZ3P0`
- `LL.DD` → `AB.12`, `MZ.99`
- `L_D_L` → `A_5_B`, `M_9_Z`
- `DDLLL` → `12ABC`, `99MNO`
- `LLS_LD` → `AB_5D`, `MZ_3P`

## Platforms Supported

✅ **Roblox** - Game platform
✅ **Instagram** - Social media
✅ **Twitter/X** - Social media
✅ **GitHub** - Developer platform
✅ **TikTok** - Video platform
✅ **Discord** - Communication platform

## Export Options

After checking completes, choose:

### 1. All Valid
Download all available usernames (VALID status only)
```
AB_123
MZ_456
CD_789
```

### 2. By Platform
Filter valid usernames by specific platform:
- All valid Roblox usernames
- All valid Instagram usernames
- All valid TikTok usernames
- etc.

**Example output** (valid_tiktok.txt):
```
AB5CD
XY9ZP
MN2LK
```

### 3. All Results
Complete results with status for each

**Example output**:
```
AB5CD - Roblox: VALID
AB5CD - Instagram: TAKEN
AB5CD - GitHub: VALID
XY9ZP - Roblox: TAKEN
XY9ZP - Twitter/X: VALID
```

## Status Codes

- ✅ **VALID** (0) - Username is available
- ❌ **TAKEN** (1) - Username is already registered
- ⛔ **CENSORED** (2) - Username contains inappropriate content (Roblox only)

## Multiple Platforms Example

Check 100 usernames with pattern `XX11` across all platforms:

1. `/snipe` 
2. Select: `XX11` pattern
3. Select: 100 usernames
4. Select: All Platforms (6 services)
5. Bot checks: 600 combinations total (100 × 6)
6. Export valid ones for each platform separately

Result: 6 files with valid usernames per service!

## Troubleshooting

### Commands not appearing
- Restart Discord or wait 1 minute
- Ensure slash commands are enabled in server settings
- Check bot has "Send Messages" permission

### "DISCORD_BOT_TOKEN not found"
- Make sure you created `.env` file
- Make sure you added your actual token
- Restart the bot

### Bot goes offline
- Check internet connection
- Check token is valid
- Look for error messages in terminal

### No results/errors
- Some platforms may have rate limits
- Try with fewer usernames
- Wait a few minutes and try again

## Environment File Security

**IMPORTANT**: The `.env` file contains your bot token!

- ✅ Added to `.gitignore` (won't be committed to Git)
- ❌ Never share your `.env` file
- ❌ Never paste your token in chat/Discord
- ❌ Regenerate token if compromised

For production, use system environment variables instead:
```bash
export DISCORD_BOT_TOKEN="your_token_here"
python discord_bot.py
```

## Need Help?

- Discord Developer Portal: https://discord.com/developers/applications
- discord.py Docs: https://discordpy.readthedocs.io/
- Python Docs: https://docs.python.org/3/


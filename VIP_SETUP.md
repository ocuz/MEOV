# VIP Setup Guide - Quick Start

## ⚡ 2-Minute VIP Setup

### Step 1: Get Discord IDs
1. Open Discord
2. Enable Developer Mode (User Settings → Advanced → Developer Mode)
3. Right-click any user
4. Select "Copy User ID"
5. Save the ID

### Step 2: Update .env File
```bash
nano .env
```

Add/update these lines:
```env
BOT_OWNER_ID=YOUR_DISCORD_ID_HERE
WHITELISTED_USER_IDS=VIP_ID_1,VIP_ID_2,VIP_ID_3
```

**Example:**
```env
BOT_OWNER_ID=123456789012345678
WHITELISTED_USER_IDS=111111111111111111,222222222222222222,333333333333333333
```

### Step 3: Restart Bot
```bash
python discord_bot.py
```

You'll see:
```
✨ VIP Users (3): 111111111111111111, 222222222222222222, 333333333333333333
✨ VIP Features Active: Unlimited Text Hunts + 10,000 per 3 days
```

---

## ✅ Verification Checklist

- [ ] Bot owner can see gold VIP embed when running `/snipe`
- [ ] Whitelisted users see "✨ VIP Username Sniper - Premium Access ✨" title
- [ ] `/help` shows different content for VIP users
- [ ] VIP users can hunt unlimited 500-letter text hunts
- [ ] VIP users get 10,000 hunts per 3 days for regular hunts
- [ ] Startup log shows VIP user IDs and feature summary

---

## 🎯 VIP Features Overview

### Unlimited Text Hunts ✨
```
Perfect for Roblox small username hunting
- Hunt 500 small letters at a time
- UNLIMITED hunts per day/week
- No cooldown between hunts
- Same-day results
```

### 10,000 Regular Hunts Per 3 Days
```
Full platform hunting across Roblox, Twitter, GitHub, TikTok, Discord
- Hunt up to 10,000 usernames in 3 days
- Automatically resets after 3 days
- All patterns available
- All platforms supported
```

### Beautiful VIP UI 👑
```
Gold-themed exclusive embeds
- "VIP 🌟" status display
- Premium feature showcase
- Special help menu for VIPs
- Priority visual branding
```

---

## 🎁 What Whitelisted Users See

### /snipe Command
```
✨ VIP USERNAME SNIPER - PREMIUM ACCESS ✨

⭐ VIP EXCLUSIVE FEATURES
✓ Text Hunts: Unlimited 500-letter custom hunts
✓ Regular Hunts: 10,000 per 3 days
✓ Priority Processing: Get results faster
✓ Advanced Patterns: All patterns available

👑 YOUR STATUS
VIP 🌟 Member
🌟 Premium Access Active
⚡ No Daily Limits on Text Hunts
```

### /help Command
```
✨ VIP HELP - PREMIUM USERNAME SNIPER ✨

🌟 VIP HUNT LIMITS
Text Hunts (Small Letters for Roblox)
↳ UNLIMITED 500-letter custom hunts 🔓
↳ Perfect for Roblox username hunting
↳ No daily/weekly limits!

Regular Hunts
↳ 10,000 hunts per 3 days
↳ Full access to all platforms
```

---

## 🚨 Common Mistakes

### ❌ Spaces in WHITELISTED_USER_IDS
```env
# WRONG!
WHITELISTED_USER_IDS=111, 222, 333

# CORRECT!
WHITELISTED_USER_IDS=111,222,333
```

### ❌ Wrong Discord ID
- Make sure you copied the USER ID, not the Channel/Server ID
- Right-click the user in chat/member list, not in settings

### ❌ Forgot to Restart Bot
- Always restart the bot after updating .env
- Changes don't apply automatically

---

## 📊 Comparison

| Feature | Normal Users | VIP Users |
|---------|------|----------|
| **Text Hunts** | ❌ | ✅ Unlimited |
| **Regular Hunts/Period** | 1,000/week | 10,000/3 days |
| **UI Theme** | Orange | Gold ⭐ |
| **Help Menu** | Basic | Premium |
| **Time to Hunt** | Faster | Instant |

---

## 🆘 Troubleshooting

**Q: VIP user not seeing gold embed?**
A: Check if their ID is in WHITELISTED_USER_IDS exactly (no spaces, correct ID)

**Q: Getting "Invalid format" error?**
A: Remove spaces from WHITELISTED_USER_IDS: `111,222,333` not `111, 222, 333`

**Q: Hunt limit not resetting?**
A: Text hunts never reset (unlimited). Regular hunts reset every 3 days automatically.

**Q: Can multiple VIP users use the same ID?**
A: No, each user needs their own unique Discord ID.

---

## 📞 Support

For issues:
1. Check `.env` is formatted correctly
2. Verify Discord IDs are correct
3. Restart the bot after changes
4. Check startup logs for VIP confirmation

---

**Version**: 0.5  
**Status**: ✅ VIP System Ready  
**Setup Time**: ~2 minutes

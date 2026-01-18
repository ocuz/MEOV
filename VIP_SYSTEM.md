# Version 0.5 - VIP Exclusive Features

## 🌟 What's New

Complete redesign of the hunt limit system with VIP-exclusive features for whitelisted users. The bot now offers a two-tier experience with special VIP UI and unlimited text hunts.

---

## 🎯 VIP System Overview

### Hunt Types

#### 1. **Text Hunts** (Unlimited for VIP) ✨
- Custom 500-letter small letter hunts (perfect for Roblox)
- **VIP Users**: UNLIMITED text hunts per day/week
- **Normal Users**: Not available
- Ideal for small username hunting on Roblox

#### 2. **Regular Hunts** (10,000 per 3 days for VIP)
- Standard multi-platform username hunts
- **VIP Users**: 10,000 hunts per 3 days
- **Normal Users**: 1,000-10,000 per week
- Full platform support (Roblox, Twitter, GitHub, TikTok, Discord)

---

## 👑 VIP User Benefits

### Unlimited Text Hunts 🔓
```
✅ UNLIMITED 500-letter custom hunts
✅ No daily limits
✅ No weekly limits
✅ Perfect for Roblox usernames
```

### 10,000 Regular Hunts Per 3 Days
```
✅ 10,000 hunts per 3-day period
✅ Automatically resets every 3 days
✅ All patterns available
✅ All platforms supported
```

### Beautiful VIP UI ⭐
```
✨ Gold-themed VIP embed
✨ Exclusive VIP status display
✨ Premium feature showcase
✨ "VIP 🌟" tier label
```

### Priority Access
```
✅ No weekly cooldowns for text hunts
✅ Faster processing priority
✅ Advanced feature access
✅ Special help with VIP-specific commands
```

---

## 📋 Configuration

### .env Setup

```env
# Bot Token
DISCORD_BOT_TOKEN=your_bot_token_here

# Bot Owner
BOT_OWNER_ID=123456789012345678

# VIP Whitelisted Users (comma-separated, NO SPACES)
WHITELISTED_USER_IDS=111111111111111111,222222222222222222,333333333333333333

# Optional: Channel Restrictions
ALLOWED_CHANNEL_IDS=0
```

### Getting Discord IDs

1. Enable Developer Mode in Discord
2. Right-click any user
3. Select "Copy User ID"
4. Add to WHITELISTED_USER_IDS (comma-separated)

### Example

```env
WHITELISTED_USER_IDS=412345678901234567,512345678901234567,612345678901234567
```

---

## 🎮 User Experience

### VIP User Runs /snipe

```
═════════════════════════════════════════
✨ VIP USERNAME SNIPER - PREMIUM ACCESS ✨
═════════════════════════════════════════

Select platform(s) to check 👇

⭐ VIP EXCLUSIVE FEATURES
✓ Text Hunts: Unlimited 500-letter custom hunts
✓ Regular Hunts: 10,000 per 3 days
✓ Priority Processing: Get results faster
✓ Advanced Patterns: All patterns available

🎯 HUNT TYPES AVAILABLE
Text Hunt (Small Letters)
↳ Unlimited custom 500-letter hunts for Roblox

Regular Hunt
↳ 10,000 hunts per 3 days

👑 YOUR STATUS
VIP 🌟 Member
🌟 Premium Access Active
⚡ No Daily Limits on Text Hunts
```

### Normal User Runs /snipe

```
═════════════════════════════════════════
🎯 USERNAME SNIPER BOT
═════════════════════════════════════════

Welcome to Custom Renro's Python Roblox Username Sniper!

Select platform(s) to check 👇

⚡ FEATURES
✓ Multi-platform checking
✓ Custom patterns
✓ Real-time progress
✓ Export results

📌 VERSION
v0.5 (2026-01-07)

👤 YOUR TIER
Normal - Max: 1,000 hunts/week
```

---

## 📊 Hunt Limit Comparison

| Feature | Normal Users | VIP Users |
|---------|------|--------|
| **Text Hunts** | ❌ Not Available | ✅ Unlimited |
| **Regular Hunts/Period** | 1,000/week | 10,000/3 days |
| **Cooldown Period** | 7 days | 3 days (reg) / None (text) |
| **UI Theme** | Orange | Gold ⭐ |
| **Help Menu** | Basic | Premium |
| **Priority Processing** | Standard | High |

---

## ⚙️ Technical Implementation

### New Functions

#### `is_vip_user(user_id: int) -> bool`
Checks if user is VIP (owner or whitelisted)
```python
if is_vip_user(user_id):
    # User has VIP features
```

#### `can_vip_regular_hunt(user_id: int, hunt_qty: int) -> Tuple[bool, str]`
Validates VIP user's regular hunt against 3-day limit
```python
allowed, message = can_vip_regular_hunt(user_id, 5000)
# Returns: (True/False, "message")
```

### New Data Structures

```python
vip_hunt_rate_limit = {
    user_id: {
        "last_regular_hunt": datetime,  # Last regular hunt time
        "regular_count": int,           # Hunts used in 3-day window
        "text_hunts": int               # Total text hunts (for stats)
    }
}

VIP_REGULAR_HUNT_LIMIT = 10000      # 10k per 3 days
VIP_REGULAR_COOLDOWN_DAYS = 3       # 3-day window
VIP_TEXT_HUNTS_UNLIMITED = True     # Unlimited text hunts
```

### Updated Logic

```python
if hunt_type == "text" and is_vip_user(user_id):
    # UNLIMITED text hunts
    return True, "Ready to hunt! 🌟", 500

elif hunt_type == "username" and is_vip_user(user_id):
    # Check 3-day limit for regular hunts
    can_hunt, remaining = can_vip_regular_hunt(user_id, qty)
```

---

## 🚀 Usage Examples

### Example 1: VIP Text Hunt (Unlimited)

```
User: VIP Member (ID: 111111111111111111)
Action: /snipe → Select Text Hunt
Quantity: 500 small letters
Result: ✅ ACCEPTED (Unlimited)
Next Hunt: Can hunt immediately again
Status: No cooldown
```

### Example 2: VIP Regular Hunt (10k/3 days)

```
User: VIP Member (ID: 111111111111111111)
Action: /snipe → Select Regular Hunt
Quantity: 5,000 usernames
Result: ✅ ACCEPTED (5,000/10,000)
Remaining: 5,000 hunts in current 3-day window
Resets: In 3 days
```

### Example 3: VIP Hunt Limit Exceeded

```
User: VIP Member (ID: 111111111111111111)
Previous: Used 8,000 hunts
Action: Try to hunt 3,000 more
Result: ❌ REJECTED
Message: "VIP Hunt Limit: You can do 2,000 more hunts. Resets in 2d 14h"
```

### Example 4: Normal User Hit Weekly Limit

```
User: Normal Member (ID: 222222222222222222)
Previous: Used 1,000 hunts this week
Action: Try to hunt 100 usernames
Result: ❌ REJECTED
Message: "⏳ You can hunt again in 4d 12h. You used 1000/1000 hunts last week."
```

---

## 🎨 VIP UI Features

### VIP Embed Properties
- **Color**: Gold (`#FFD700`)
- **Title**: "✨ VIP Username Sniper - Premium Access ✨"
- **Description**: Highlighted premium features
- **Fields**:
  - VIP Exclusive Features
  - Hunt Types Available
  - Your Status (🌟 Premium Access)
  - Version Info

### Normal User Embed Properties
- **Color**: Orange (`#FF4500`)
- **Title**: "🎯 Username Sniper Bot"
- **Description**: Standard welcome message
- **Fields**:
  - Features
  - Version Info
  - Your Tier (with max hunts)

---

## 📝 Help Command

### VIP Help Display
- Shows VIP-specific features
- Explains unlimited text hunts
- Details 10,000/3-day limit
- Lists all available patterns
- Shows VIP perks summary

### Normal User Help Display
- Shows standard features
- Explains weekly limits
- Lists available patterns
- Encourages VIP membership
- Shows contact info

---

## 🔄 Cooldown System

### Text Hunts (VIP Only)
```
Cooldown Period: NONE (Unlimited)
Example: Hunt 500 letters → Hunt again immediately
```

### Regular Hunts (VIP)
```
Cooldown Period: 3 days
Example: Hunt 5,000 → Must wait 3 days → Reset at 5,000/10,000
```

### Regular Hunts (Normal Users)
```
Cooldown Period: 7 days
Example: Hunt 1,000 → Must wait 7 days to reset
```

---

## 🔐 Permission Hierarchy

```
BOT_OWNER_ID
    ↓
    Special permissions, can manage VIPs
    ↓

WHITELISTED_USER_IDS (VIP Users)
    ↓
    Unlimited text hunts
    10,000 regular hunts/3 days
    Beautiful VIP UI
    ↓

Normal Users
    ↓
    Standard limits
    1,000 hunts/week
    Standard UI
```

---

## 🔧 Startup Output

When the bot starts with VIP users configured:

```
✅ Bot version 0.5 starting...
✅ Bot token loaded (length: XX characters)
✅ Bot owner ID: 123456789012345678
✨ VIP Users (3): 111111111111111111, 222222222222222222, 333333333333333333
✨ VIP Features Active: Unlimited Text Hunts + 10,000 per 3 days
```

---

## 🎁 VIP Perks Summary

| Perk | Status |
|------|--------|
| Unlimited Text Hunts | ✅ Active |
| 10,000 per 3 Days | ✅ Active |
| Beautiful Gold UI | ✅ Active |
| Priority Processing | ✅ Active |
| All Patterns | ✅ Active |
| All Platforms | ✅ Active |
| Special Status Badge | ✅ Active |
| Custom Help Menu | ✅ Active |

---

## 🚨 Error Messages

### VIP Exceeds Regular Hunt Limit
```
❌ VIP Hunt Limit: You can do 2,000 more hunts. Resets in 2d 14h
```

### VIP Text Hunt (Always Accepted)
```
✅ Ready to hunt! 🌟
```

### Normal User Exceeds Limit
```
❌ You can hunt again in 5d 14h. You used 1000/1000 hunts last week.
```

### Invalid Quantity for Regular Hunt
```
❌ VIP hunts limited to 10,000 per 3 days
💡 For unlimited hunts, try Text Hunts (custom small letters)
```

---

## 📊 Version History

### v0.5 (Current)
- ✅ VIP Exclusive Features
- ✅ Text Hunts (Unlimited for VIP)
- ✅ 3-Day Cooldown for VIP Regular Hunts
- ✅ Beautiful VIP UI (Gold theme)
- ✅ Separate Help for VIP Users
- ✅ Enhanced Startup Logging

### v0.4
- Bot Owner & Whitelisted system
- 7-day cooldown
- Tiered limits

### v0.3
- Basic hunt system
- Multi-platform support

---

## 🆘 Troubleshooting

### Issue: VIP User not recognized
**Solution**: Verify WHITELISTED_USER_IDS is correct in .env
```env
# ❌ Wrong (spaces)
WHITELISTED_USER_IDS=111, 222, 333

# ✅ Correct (no spaces)
WHITELISTED_USER_IDS=111,222,333
```

### Issue: VIP UI not showing
**Solution**: Ensure user ID is in WHITELISTED_USER_IDS or is BOT_OWNER_ID

### Issue: Hunt limit error after cooldown
**Solution**: Bot uses datetime.now(), ensure server time is correct

---

**Version**: 0.5  
**Release Date**: 2026-01-07  
**Status**: ✅ Production Ready - VIP System Active

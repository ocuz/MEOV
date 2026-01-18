# Version 0.4 Update Summary

## Overview
Successfully updated the Username Sniper Bot with tiered hunt rate limiting system and enhanced user management. Bot owner and whitelisted users now get elevated hunting quotas with weekly cooldowns.

---

## Key Features Added

### 1. **Tiered Hunt Rate Limiting** 🎯
- **Bot Owner**: 50,000 hunts per week
- **Whitelisted Users**: 50,000 hunts per week
- **Normal Users**: 1,000-10,000 hunts per week
- **Weekly Cooldown**: Automatic reset every 7 days

### 2. **User Permission System** 👑
Three-tier permission hierarchy:
```
Owner (highest) → Whitelisted → Normal (default)
```

### 3. **Hunt Tracking & Enforcement** 📊
- Real-time validation of hunt limits before command execution
- Automatic cooldown calculation with remaining time display
- Hunt counter tracking within the 7-day window
- Automatic limit reset after cooldown period

### 4. **Enhanced User Feedback** 📈
- User tier displayed in `/snipe` command
- Hunt limit information shown in `/help` command
- Tier-based error messages with maximum quantities
- Visual tier badge in embeds

### 5. **Configuration Support** ⚙️
Two new environment variables:
```env
BOT_OWNER_ID=123456789           # Owner's Discord ID
WHITELISTED_USER_IDS=111,222,333 # Comma-separated whitelisted user IDs
```

---

## Implementation Details

### New Functions

#### `get_user_permission_tier(user_id: int) -> str`
Determines a user's permission tier for rate limiting.
```python
# Returns: "owner" | "whitelisted" | "normal"
```

#### `can_hunt(user_id: int, hunt_type: str = "username") -> Tuple[bool, str, int]`
Validates if user can hunt and returns:
- `bool`: Whether hunt is allowed
- `str`: Message (error or confirmation)
- `int`: Maximum quantity allowed for this user
```python
allowed, message, max_qty = can_hunt(user_id)
```

### Modified Components

| Component | Changes |
|-----------|---------|
| `discord_bot.py` | Added version tracking (v0.4), rate limiting logic, permission checks |
| `CustomQuantityModal` | Added hunt limit validation before accepting quantity |
| `/snipe` command | Added permission check before allowing hunt to start |
| `/help` command | Added hunt limits table and user tier information |
| Startup logging | Added version and owner/whitelist info to console output |

### New Data Structures

```python
hunt_rate_limit = {
    user_id: {
        "last_hunt": datetime,  # When the user last hunted
        "count": int            # Total hunts used in current window
    }
}

HUNT_LIMITS = {
    "owner": 50000,
    "whitelisted": 50000,
    "sniper": 10000,
    "normal": 1000
}
```

---

## Configuration Guide

### Step 1: Update .env File
```bash
nano .env
```

### Step 2: Add Your Settings
```env
DISCORD_BOT_TOKEN=your_token_here
BOT_OWNER_ID=123456789012345678
WHITELISTED_USER_IDS=111111111111111111,222222222222222222,333333333333333333
```

### Step 3: Restart Bot
```bash
python discord_bot.py
```

You should see:
```
✅ Bot version 0.4 starting...
✅ Bot token loaded (length: XX characters)
✅ Bot owner ID: 123456789012345678
✅ Whitelisted users: 3
```

---

## User Experience

### Before (v0.3)
- All users could hunt up to 10,000 usernames at once
- No cooldown or weekly limits
- No tier differentiation

### After (v0.4)
- **Owner**: "✅ Set to 50,000 usernames" (full weekly allowance)
- **Whitelisted**: "✅ Set to 50,000 usernames" (full weekly allowance)
- **Normal**: "✅ Set to 1,000 usernames" (limited quota)

When limit exceeded:
```
❌ You can hunt again in 5d 14h. You used 1000/1000 hunts last week.
```

---

## Testing Checklist

- [x] Version number updated to 0.4
- [x] Rate limiting logic implemented and enforced
- [x] Permission tiers correctly assigned
- [x] Hunt counter tracking working
- [x] 7-day cooldown calculation accurate
- [x] Error messages display remaining time
- [x] User tier visible in `/snipe` embed
- [x] Hunt limits shown in `/help` command
- [x] Startup logging displays owner/whitelisted info
- [x] CHANGELOG.md created with full details

---

## Files Modified/Created

| File | Status | Details |
|------|--------|---------|
| [discord_bot.py](discord_bot.py) | ✅ Modified | Core bot with rate limiting |
| [CHANGELOG.md](CHANGELOG.md) | ✅ Created | Complete version history |
| UPDATE_SUMMARY.md | ✅ Created | This file |

---

## Future Enhancements

Potential improvements for future versions:

1. **Persistent Storage**: Save hunt history to database
2. **Hunt Analytics**: Per-user statistics and metrics
3. **Custom Limits**: Admin override for individual users
4. **Purchase System**: Users can buy additional hunts
5. **Audit Logs**: Track all hunt activities for review
6. **GraphQL API**: Check hunt status programmatically
7. **Web Dashboard**: Visual interface for managing limits

---

## Support & Troubleshooting

### Issue: "Invalid WHITELISTED_USER_IDS format"
**Solution**: Ensure user IDs are comma-separated with no spaces:
```env
# ❌ Wrong
WHITELISTED_USER_IDS=111, 222, 333

# ✅ Correct
WHITELISTED_USER_IDS=111,222,333
```

### Issue: Users see "You can hunt again in" message
**Solution**: Their 7-day hunt window hasn't expired. They'll need to wait.

### Issue: Owner not recognized
**Solution**: Verify BOT_OWNER_ID is set correctly:
1. Right-click user in Discord
2. Copy User ID
3. Paste into BOT_OWNER_ID in .env

---

**Version**: 0.4  
**Release Date**: 2026-01-07  
**Author**: Custom Renro  
**Status**: ✅ Production Ready

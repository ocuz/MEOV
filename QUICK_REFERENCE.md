# Quick Reference - v0.4 Hunt Limits

## Hunt Quota System (Weekly Reset)

### User Tiers & Limits

```
┌─────────────────┬──────────┬──────────────┐
│ User Type       │ Hunts/Wk │ Config Var   │
├─────────────────┼──────────┼──────────────┤
│ Owner (You)     │ 50,000   │ BOT_OWNER_ID │
│ Whitelisted     │ 50,000   │ WHITELIST_*  │
│ Normal Users    │  1,000   │ (default)    │
└─────────────────┴──────────┴──────────────┘
```

### Cooldown & Reset
- **Duration**: 7 days from first hunt
- **Reset**: Automatic after 7 days
- **Status Check**: Use `/help` to see your tier and remaining hunts

---

## Configuration (.env)

```env
# Owner Discord ID (get by right-clicking user → Copy User ID)
BOT_OWNER_ID=123456789012345678

# Whitelisted users (comma-separated, no spaces)
WHITELISTED_USER_IDS=111111111111111111,222222222222222222

# Existing configs still work
DISCORD_BOT_TOKEN=your_token
ALLOWED_CHANNEL_IDS=0
```

---

## Examples

### Owner Hunt (50,000 max)
```
/snipe
→ Select platforms
→ Custom Quantity: 50000 ✅ ALLOWED

Next hunt available: In 7 days
```

### Normal User Hunt (1,000 max)
```
/snipe
→ Select platforms
→ Custom Quantity: 5000 ❌ REJECTED (exceeds 1,000 limit)
→ Custom Quantity: 1000 ✅ ALLOWED

Next hunt available: In 7 days
```

### Within 7-Day Window
```
❌ You can hunt again in 5d 14h. 
   You used 1000/1000 hunts last week.
```

---

## Commands

### `/snipe` - Start hunting
- Shows your tier and max hunts/week
- Enforces rate limits
- Requires available hunt quota

### `/help` - View details
- Shows all tier limits
- Displays your current tier
- Explains patterns and exports

---

## Error Messages

| Scenario | Message |
|----------|---------|
| First hunt | "✅ Ready to hunt!" |
| Exceeded limit | "❌ You can hunt again in Xd Yh. You used Z/1000 hunts last week." |
| Invalid quantity | "❌ Please enter between 1-1000. Normal users can hunt up to 1,000 usernames at a time." |

---

## Key Files

- **discord_bot.py**: Main bot with rate limiting logic
- **CHANGELOG.md**: Complete version history
- **UPDATE_SUMMARY.md**: Detailed implementation guide
- **.env**: Configuration file (create/update as needed)

---

## Setup Steps (30 seconds)

1. **Get Discord IDs**
   - Right-click any user → "Copy User ID"

2. **Update .env**
   ```bash
   nano .env
   # Add BOT_OWNER_ID and WHITELISTED_USER_IDS
   ```

3. **Restart Bot**
   ```bash
   python discord_bot.py
   ```

4. **Verify**
   - Check console for "✅ Bot owner ID: XXX"
   - Use `/help` to see your limits

---

## Troubleshooting

**Q: Owner not recognized?**
A: Verify BOT_OWNER_ID matches your Discord ID exactly

**Q: Invalid whitelist format error?**
A: Use comma-separated IDs with no spaces: `111,222,333`

**Q: How to change limits?**
A: Edit HUNT_LIMITS dict in discord_bot.py (requires bot restart)

---

**Version**: 0.4 | **Released**: 2026-01-07 | **Status**: ✅ Ready to Use

# VIP System v0.5 - Quick Reference Card

## 🎯 VIP Limits at a Glance

```
╔════════════════════════════════════════════════════════════╗
║           WHITELISTED USER (VIP) FEATURES                  ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  TEXT HUNTS (Small Letters - Roblox)                      ║
║  ├─ Limit: UNLIMITED ∞                                    ║
║  ├─ Size: 500 letters per hunt                            ║
║  └─ Cooldown: NONE (hunt again immediately!)              ║
║                                                            ║
║  REGULAR HUNTS (All Platforms)                            ║
║  ├─ Limit: 10,000 per 3 days                              ║
║  ├─ Cooldown: 3 days (auto-reset)                         ║
║  └─ Platforms: Roblox, Twitter, GitHub, TikTok, Discord   ║
║                                                            ║
║  UI THEME: Gold (#FFD700) ✨                              ║
║  STATUS: "VIP 🌟 Member"                                  ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

---

## ⚙️ .env Configuration

```env
# Required for VIP system
BOT_OWNER_ID=YOUR_DISCORD_ID
WHITELISTED_USER_IDS=ID1,ID2,ID3

# Format: Comma-separated, NO SPACES
# Example: 111111111111111111,222222222222222222
```

---

## 🎯 Hunt Selection

When VIP user runs `/snipe`:

```
📌 CHOOSE HUNT TYPE:
├─ Text Hunt → UNLIMITED 500-letter hunts
├─ Regular Hunt → 10,000 per 3 days
└─ Both available (select platforms)
```

---

## 📊 Limits Table

| Hunt Type | Limit | Cooldown | UI |
|-----------|-------|----------|-----|
| Text | ∞ Unlimited | None | Gold ✨ |
| Regular | 10,000 | 3 days | Gold ✨ |
| Normal Text | ❌ Blocked | N/A | Orange |
| Normal Regular | 1,000/week | 7 days | Orange |

---

## 🌟 VIP UI Preview

```
Title: ✨ VIP USERNAME SNIPER - PREMIUM ACCESS ✨
Color: Gold (#FFD700)

⭐ VIP EXCLUSIVE FEATURES
✓ Text Hunts: Unlimited 500-letter custom hunts
✓ Regular Hunts: 10,000 per 3 days
✓ Priority Processing
✓ Advanced Patterns

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

---

## ✅ Verification Steps

1. **Update .env**
   ```bash
   nano .env
   # Add WHITELISTED_USER_IDS=YOUR_VIP_IDS
   ```

2. **Restart Bot**
   ```bash
   python discord_bot.py
   ```

3. **Check Startup Log**
   ```
   ✨ VIP Users (3): [IDs listed]
   ✨ VIP Features Active: Unlimited Text Hunts + 10,000 per 3 days
   ```

4. **Test VIP Command**
   - VIP user runs `/snipe`
   - Should see GOLD embed (not orange)
   - Should show "VIP 🌟" status

5. **Test Limits**
   - Text hunt: Can hunt unlimited times
   - Regular hunt: Can do 10,000 in 3 days

---

## 🚨 Troubleshooting Checklist

- [ ] WHITELISTED_USER_IDS has NO SPACES
- [ ] Discord ID is correct (copied from Discord)
- [ ] Bot restarted after .env update
- [ ] VIP user sees GOLD embed (not orange)
- [ ] Startup log shows VIP users listed
- [ ] VIP can hunt text immediately after

---

## 📞 Quick Help

**Q: VIP not seeing gold embed?**
A: Check ID in WHITELISTED_USER_IDS matches their Discord ID exactly

**Q: "Invalid format" in startup?**
A: Remove all spaces: `111,222,333` not `111, 222, 333`

**Q: How to get Discord ID?**
A: Right-click user in Discord → "Copy User ID"

**Q: Can VIP hunt text infinitely?**
A: YES! Text hunts are completely unlimited

**Q: When do regular hunts reset?**
A: Every 3 days automatically

---

## 🎁 Command Guide for VIPs

```
/snipe
├─ See beautiful gold embed
├─ Choose Text Hunt (unlimited)
├─ Or choose Regular Hunt (10k/3 days)
└─ Select platforms and hunt!

/help
├─ See VIP-exclusive help
├─ Shows unlimited text hunt info
├─ Shows 10k/3 days info
└─ Displays all VIP perks
```

---

## 📈 Comparison

```
NORMAL USER          vs          VIP USER
─────────────────────────────────────────────
1,000/week hunts                10,000/3 days
7-day cooldown                  3-day cooldown
No text hunts                   ∞ Text hunts
Orange UI                       Gold UI ✨
Standard help                   Premium help
```

---

**Version**: 0.5  
**Date**: 2026-01-07  
**Status**: ✅ Ready to Configure

---

## 📚 Full Documentation

- **VIP_SYSTEM.md** - Complete features guide
- **VIP_SETUP.md** - Step-by-step setup (2 min)
- **VIP_UPDATE_COMPLETE.md** - Full update details
- **CHANGELOG.md** - Version history

---

**Need Help?** → Check VIP_SETUP.md for guided setup!

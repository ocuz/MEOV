# 📋 CLI vs Discord Bot Comparison

## File Comparison

| Feature | main.py (CLI) | discord_bot.py (Discord) |
|---------|---------------|------------------------|
| **Interface** | Terminal prompts | Discord buttons/menus |
| **Patterns** | 7 patterns | 15 patterns + custom |
| **Alphabet Combos** | Basic (L, D) | Extended (L, l, D, S) |
| **Export** | 3 text files | Multiple format options |
| **Multi-user** | Single session | Per-user sessions |
| **Real-time** | Shows results as checks | Progress bar + results |
| **Symbols** | None | Dots (.), underscores (_), dashes (-) |

## Pattern Examples

### Basic Patterns (Both)
- `X_XXX` → `A_BCD`
- `XX_XX` → `AB_CD`
- `XXX_X` → `ABC_D`

### Extended Patterns (Discord Bot Only)
- `XX11` → `AB12` (2 letters + 2 digits)
- `1X1X1X` → `5A9B3C` (Alternating)
- `X.X.X` → `A.B.C` (Dot-separated)
- `X_X_X` → `A_B_C` (Underscore-separated)
- `XX1XX` → `AB5CD` (Mixed arrangement)

### Custom Patterns

**CLI Format** (main.py):
```
L = Letter
D = Digit
Example: LLDLD → AB5C9
```

**Discord Format** (discord_bot.py):
```
L = Uppercase Letter (A-Z)
l = Lowercase Letter (a-z)
D = Digit (0-9)
S = Symbol (_.-) 
Example: LL.DD → AB.12, MZ.99
Example: LLS_LD → AB_5D, MZ_3P
```

## Alphabet Combinations

### CLI (main.py)
```
Letters: A-Z (uppercase only)
Digits: 0-9
No symbols supported
```

### Discord Bot (discord_bot.py)
```
Uppercase Letters: A-Z
Lowercase Letters: a-z
Digits: 0-9
Symbols: _ (underscore), . (dot), - (dash)
Separators: Underscore, dot, or dash in patterns
```

## Export/Results

### CLI Results (main.py)
Creates 3 files:
- `valid.txt` - Available usernames
- `taken.txt` - Taken usernames
- `censored.txt` - Censored usernames

Each file lists usernames with platform in parentheses.

### Discord Bot Results (discord_bot.py)
Downloads as files with filtering options:
- **All Valid** - All available usernames (VALID status)
- **By Platform** - Filter to specific service:
  - `valid_roblox.txt`
  - `valid_instagram.txt`
  - `valid_tiktok.txt`
  - `valid_twitter.txt`
  - `valid_github.txt`
  - `valid_discord.txt`
- **All Results** - Complete status for each

## Services Checked

Both check these platforms:
✅ Roblox
✅ Instagram
✅ Twitter/X
✅ GitHub
✅ TikTok
✅ Discord

**Difference**: Discord bot lets you check all at once and filter results by service!

## Usage Example

### Same Scenario, Different Approaches

**Scenario**: Check 250 usernames with pattern `XX11` on all platforms

#### CLI Approach (main.py)
```bash
$ python main.py
Choose a pattern: 
> [can't see new patterns, only 1-9]
Enter your choice: 8
Enter custom pattern: XX11
How many usernames to check? 250
SELECT PLATFORM(S) TO CHECK:
1. Roblox
...
7. All Platforms
Enter platform choice: 7
[Checking...]
Results saved to valid.txt, taken.txt, censored.txt
```

#### Discord Approach (discord_bot.py)
```
User: /snipe
Bot: Shows 15 pattern options (including XX11)
User: Selects "XX11"
Bot: Shows quantity buttons (100, 250, 500, Custom)
User: Clicks "250"
Bot: Shows platform multi-select
User: Selects "All Platforms"
Bot: Shows "Start Checking" button
User: Clicks it
Bot: Live progress updates, then shows results
User: Clicks "By Platform" export
Bot: Select TikTok → Downloads valid_tiktok.txt
Bot: Select Roblox → Downloads valid_roblox.txt
```

## Setup Differences

### CLI (main.py)
```bash
pip install requests colorama
python main.py
```

### Discord Bot (discord_bot.py)
```bash
cp .env.example .env
# Edit .env and add your bot token
pip install -r requirements.txt
python discord_bot.py
```

## Which Should You Use?

**Use main.py (CLI) if you**:
- Want quick terminal-based checks
- Don't have a Discord server
- Prefer simple, direct interaction
- Don't need advanced filtering

**Use discord_bot.py if you**:
- Have a Discord server
- Want beautiful UI with buttons/menus
- Need advanced export/filtering options
- Want to share with multiple users
- Like real-time progress updates
- Want more alphabet combo options

Both tools are powerful and complementary! 🚀

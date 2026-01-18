# === Proxy Support for Social Username Checker ===
import itertools
import discord
from discord.ext import commands
from discord import app_commands
import random
import string
import requests
import asyncio
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import os
from pathlib import Path
from dotenv import load_dotenv
import json
import io

def load_proxies(proxy_file="proxies.txt"):
    proxies = []
    try:
        with open(proxy_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    proxies.append(line)
    except Exception as e:
        print(f"[ProxyLoader] Could not load proxies: {e}")
    return proxies

def get_proxy_dict(proxy_ip):
    return {"http": f"http://{proxy_ip}", "https": f"http://{proxy_ip}"}

# ==================== MULTI-PLATFORM SOCIAL USERNAME CHECKER (v1.0) ====================

SOCIAL_PLATFORMS = {
    "Instagram": "https://www.instagram.com/{}/",
    "TikTok": "https://www.tiktok.com/@{}",
    "Twitter": "https://www.twitter.com/{}/",
    "YouTube": "https://www.youtube.com/user/{}"
}

SOCIAL_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

SOCIALHUNT_MIN_DELAY = 1.0
SOCIALHUNT_MAX_DELAY = 3.0

def rgb_gradient_color(idx: int, total: int) -> discord.Color:
    # Simple RGB gradient (red to green to blue)
    if total <= 1:
        return discord.Color.default()
    ratio = idx / (total - 1)
    if ratio < 0.5:
        # Red to Green
        r = int(255 * (1 - 2 * ratio))
        g = int(255 * (2 * ratio))
        b = 0
    else:
        # Green to Blue
        r = 0
        g = int(255 * (2 - 2 * ratio))
        b = int(255 * (2 * ratio - 1))
    return discord.Color.from_rgb(r, g, b)



# Load environment variables
load_dotenv()

# Version
BOT_VERSION = "1.0"
BOT_VERSION_DATE = "2026-01-18"

# Configuration
ALLOWED_CHANNEL_IDS = []
BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID", "0"))  # Set this in .env
WHITELISTED_USERS = []  # Set this in .env as comma-separated IDs (VIP users)
AUTO_WHITELIST_ROLE_ID = 1460427206928109659  # Automatically treat this role as a VIP
whitelisted_env = os.getenv("WHITELISTED_USER_IDS", "0")
if whitelisted_env != "0":
    try:
        WHITELISTED_USERS = [int(uid.strip()) for uid in whitelisted_env.split(",")]
    except ValueError:
        print("⚠️  Invalid WHITELISTED_USER_IDS format.")
channel_ids_env = os.getenv("ALLOWED_CHANNEL_IDS", "0")
if channel_ids_env != "0":
    try:
        ALLOWED_CHANNEL_IDS = [int(cid.strip()) for cid in channel_ids_env.split(",")]
    except ValueError:
        print("⚠️  Invalid ALLOWED_CHANNEL_IDS format. Using all channels.")

# Animations
SPINNER = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
PROGRESS_FULL = "█"
PROGRESS_EMPTY = "░"

# X API Configuration (Official Twitter/X API v2)
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN", "")  # X API v2 Bearer Token for batch checking
X_API_ENDPOINT = "https://api.twitter.com/2/users/by"
X_BATCH_SIZE = 100  # Max usernames per request (official API limit)

# Rate limiting for Twitter API
twitter_rate_limit = {}  # {user_id: {"requests": []}}
TWITTER_MAX_REQUESTS_PER_MINUTE = 100
TWITTER_CONCURRENT_USERS = set()  # Track concurrent users checking Twitter
TWITTER_MAX_CONCURRENT_USERS = 9

# VIP Twitter Rate Limiting (100 requests per hour for VIP users using X API)
vip_twitter_rate_limit = {}  # {user_id: {"requests": [], "hour_start": datetime}}
VIP_TWITTER_MAX_REQUESTS_PER_HOUR = 100
VIP_TWITTER_COOLDOWN_MINUTES = 60

# Hunt quantity limits (per session)
HUNT_LIMITS = {
    "owner": 50000,      # Bot owner can do 50k hunts
    "whitelisted": 50000,  # Whitelisted users can do 50k hunts
    "sniper": 10000,     # Normal users can do 10k sniper hunts
    "normal": 1000       # Normal users can do 1k normal hunts
}

# VIP Text Hunt tracking (for whitelisted users only - small letter Roblox hunts)
# Text hunts: unlimited 500-letter custom hunts
VIP_TEXT_HUNTS_UNLIMITED = True  # Unlimited text hunts for VIP users

# Hunt type tracking
HUNT_TYPE_LIMITS = {
    "username": HUNT_LIMITS,
    "sniper": HUNT_LIMITS,
    "text": {"vip": float('inf'), "normal": 0}  # Text hunts only for VIP
}

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
# intents.members = True  # Not needed for role checking in interactions
bot = commands.Bot(command_prefix="!", intents=intents)

# User sessions to track results
user_sessions: Dict[int, Dict] = {}

def member_has_auto_whitelist_role(member: Optional[discord.Member]) -> bool:
    """Return True if the member has the auto-whitelist role"""
    if not member:
        return False
    roles = getattr(member, "roles", None)
    if not roles:
        return False
    return any(role.id == AUTO_WHITELIST_ROLE_ID for role in roles)

def get_user_permission_tier(user_id: int, member: Optional[discord.Member] = None) -> str:
    """Determine user's permission tier for rate limits"""
    if user_id == BOT_OWNER_ID:
        return "owner"
    if member_has_auto_whitelist_role(member):
        return "whitelisted"
    elif user_id in WHITELISTED_USERS:
        return "whitelisted"
    else:
        return "normal"

def is_vip_user(user_id: int, member: Optional[discord.Member] = None) -> bool:
    """Check if user is VIP (whitelisted or owner)"""
    if user_id == BOT_OWNER_ID:
        return True
    if member_has_auto_whitelist_role(member):
        return True
    return user_id in WHITELISTED_USERS

def can_hunt(user_id: int, hunt_type: str = "username", member: Optional[discord.Member] = None) -> Tuple[bool, str, int]:
    """Check if user can perform a hunt. Returns (allowed, message, max_quantity)"""
    permission_tier = get_user_permission_tier(user_id, member)

    # Special handling for VIP text hunts (unlimited for whitelisted users)
    if hunt_type == "text" and is_vip_user(user_id, member):
        return True, "Ready to hunt! 🌟", 500

    max_qty = HUNT_TYPE_LIMITS[hunt_type][permission_tier]
    return True, "Ready to hunt!", max_qty

class UsernameChecker:
    """Handles all username checking logic"""
    
    @staticmethod
    def check_twitter_rate_limit(user_id):
        """Check if user has exceeded Twitter API rate limit (100 requests/minute)"""
        now = datetime.now()
        
        # Initialize user's rate limit tracker if not exists
        if user_id not in twitter_rate_limit:
            twitter_rate_limit[user_id] = {"requests": []}
        
        # Remove requests older than 1 minute
        twitter_rate_limit[user_id]["requests"] = [
            req_time for req_time in twitter_rate_limit[user_id]["requests"]
            if (now - req_time).total_seconds() < 60
        ]
        
        # Check if limit exceeded
        if len(twitter_rate_limit[user_id]["requests"]) >= TWITTER_MAX_REQUESTS_PER_MINUTE:
            return False  # Rate limit exceeded
        
        # Add current request
        twitter_rate_limit[user_id]["requests"].append(now)
        return True  # Request allowed
    
    @staticmethod
    def gen_pat_digit(val=None, strict=False):
        while True:
            if val is None:
                val = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            has_digit = any(c.isdigit() for c in val)
            has_alpha = any(c.isalpha() for c in val)
            if has_digit and (not strict or has_alpha):
                return val
            val = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    
    @staticmethod
    def gen_mixed_4():
        """Generate 4-character mixed pattern with letters and numbers"""
        while True:
            val = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            has_digit = any(c.isdigit() for c in val)
            has_alpha = any(c.isalpha() for c in val)
            if has_digit and has_alpha:
                return val
    
    @staticmethod
    def gen_mixed_5():
        """Generate 5-character mixed pattern with letters and numbers"""
        while True:
            val = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            has_digit = any(c.isdigit() for c in val)
            has_alpha = any(c.isalpha() for c in val)
            if has_digit and has_alpha:
                return val

    @staticmethod
    def rand_char(c):
        if c == "L":
            return random.choice(string.ascii_uppercase)
        elif c == "D":
            return random.choice(string.digits)
        elif c == "S":
            return random.choice("_.-")
        elif c == "l":
            return random.choice(string.ascii_lowercase)
        return c

    @staticmethod
    def gen_from_fmt(fmt):
        return ''.join(UsernameChecker.rand_char(c) for c in fmt)

    # Platform checking functions
    @staticmethod
    async def chk_roblox(username):
        """Check Roblox availability"""
        url = f"https://auth.roblox.com/v1/usernames/validate?username={username}&birthday=2001-09-11"
        try:
            response = await asyncio.to_thread(requests.get, url, timeout=5)
            if response.status_code == 200:
                code = response.json().get("code")
                return code
        except:
            pass
        return None

    @staticmethod
    async def chk_twitter(username, user_id=None, use_x_api=False):
        """Check Twitter/X availability with concurrent user limit and optional X API v2 support"""
        try:
            # Check if we can accept another user checking Twitter
            if user_id:
                # If this user is not yet in concurrent set, add them
                is_new_user = user_id not in TWITTER_CONCURRENT_USERS
                
                if is_new_user and len(TWITTER_CONCURRENT_USERS) >= TWITTER_MAX_CONCURRENT_USERS:
                    return None  # Max concurrent users reached, skip this check
                
                if is_new_user:
                    TWITTER_CONCURRENT_USERS.add(user_id)
                
                # Check rate limit
                if not UsernameChecker.check_twitter_rate_limit(user_id):
                    return None  # Rate limited
            
            url = f"https://api.twitter.com/2/users/by/username/{username}"
            response = await asyncio.to_thread(requests.get, url, timeout=5)
            if response.status_code == 404:
                return 0
            elif response.status_code == 200:
                return 1
        except:
            pass
        return None
    
    @staticmethod
    async def chk_twitter_batch(usernames: List[str], user_id: int = None) -> Dict[str, int]:
        """Check multiple Twitter usernames using official X API v2 batch endpoint
        
        VIP users: 100 requests/hour limit (most efficient for bulk checking)
        Requires X_BEARER_TOKEN to be set in .env
        
        Returns: {username: status} where status is 0 (available), 1 (taken), or None (error)
        """
        if not X_BEARER_TOKEN:
            return {username: None for username in usernames}
        
        # Check VIP rate limit if user specified
        if user_id and is_vip_user(user_id):
            # Count as batch request (100 usernames = 1 request quota)
            allowed, msg, remaining = TwitterXAPIChecker.check_vip_twitter_rate_limit(user_id, 1)
            if not allowed:
                return {username: None for username in usernames}  # Over limit
        
        # Use X API batch checker
        return await TwitterXAPIChecker.batch_check_twitter_usernames(usernames, X_BEARER_TOKEN)

    @staticmethod
    async def chk_github(username):
        """Check GitHub availability"""
        try:
            url = f"https://api.github.com/users/{username}"
            response = await asyncio.to_thread(requests.get, url, timeout=5)
            if response.status_code == 404:
                return 0
            elif response.status_code == 200:
                return 1
        except:
            pass
        return None

    @staticmethod
    async def chk_tiktok(username):
        """Check TikTok availability"""
        try:
            url = f"https://www.tiktok.com/@{username}"
            response = await asyncio.to_thread(requests.head, url, timeout=5, allow_redirects=False)
            if response.status_code == 404:
                return 0
            elif response.status_code == 200:
                return 1
        except:
            pass
        return None

    @staticmethod
    async def chk_discord(username):
        """Check Discord availability"""
        try:
            url = f"https://discordapp.com/api/v9/users/{username}"
            response = await asyncio.to_thread(requests.get, url, timeout=5)
            if response.status_code == 404:
                return 0
            elif response.status_code == 200:
                return 1
        except:
            pass
        return None


class TwitterXAPIChecker:
    """Official X API v2 batch username checker for efficient sniping"""
    
    @staticmethod
    def check_vip_twitter_rate_limit(user_id: int, request_count: int = 1) -> Tuple[bool, str, int]:
        """Check if VIP user has exceeded 100 requests/hour limit for X API
        
        Returns: (allowed: bool, message: str, requests_remaining: int)
        """
        now = datetime.now()
        
        # Initialize VIP Twitter rate limit tracker
        if user_id not in vip_twitter_rate_limit:
            vip_twitter_rate_limit[user_id] = {
                "requests": [],
                "hour_start": now
            }
        
        vip_data = vip_twitter_rate_limit[user_id]
        hour_start = vip_data["hour_start"]
        
        # Check if we're in a new hour
        if (now - hour_start).total_seconds() >= 3600:
            # Reset for new hour
            vip_twitter_rate_limit[user_id] = {
                "requests": [],
                "hour_start": now
            }
            vip_data = vip_twitter_rate_limit[user_id]
        
        current_requests = len(vip_data["requests"])
        requests_remaining = VIP_TWITTER_MAX_REQUESTS_PER_HOUR - current_requests
        
        # Check if this request would exceed limit
        if current_requests + request_count > VIP_TWITTER_MAX_REQUESTS_PER_HOUR:
            minutes_until_reset = 60 - int((now - hour_start).total_seconds() / 60)
            return False, f"❌ Twitter X API Rate Limit: You can do {requests_remaining} more requests this hour. Resets in {minutes_until_reset}m", requests_remaining
        
        # Add request timestamps
        for _ in range(request_count):
            vip_data["requests"].append(now)
        
        return True, "✅ X API Request Allowed", requests_remaining - request_count
    
    @staticmethod
    async def batch_check_twitter_usernames(usernames: List[str], bearer_token: str) -> Dict[str, int]:
        """
        Check multiple Twitter usernames in a single X API v2 request (up to 100)
        
        Returns dict: {username: status}
        - 0 = AVAILABLE (Not Found)
        - 1 = TAKEN (Found)
        - 2 = BANNED/RESTRICTED (Not Found but may be suspended account)
        - None = ERROR
        """
        if not bearer_token or not usernames:
            return {username: None for username in usernames}
        
        try:
            # Prepare batch request
            usernames_param = ",".join(usernames[:X_BATCH_SIZE])
            
            headers = {
                "Authorization": f"Bearer {bearer_token}",
                "User-Agent": "MEOV-Sniper-v0.5"
            }
            
            url = f"{X_API_ENDPOINT}?usernames={usernames_param}"
            
            # Make async request
            response = await asyncio.to_thread(
                requests.get, 
                url, 
                headers=headers, 
                timeout=10
            )
            
            results = {}
            
            if response.status_code == 200:
                data = response.json()
                
                # Usernames in 'data' array = TAKEN
                if "data" in data:
                    for user_obj in data["data"]:
                        results[user_obj.get("username", "").lower()] = 1  # TAKEN
                
                # Usernames in 'errors' with "Not Found Error" = AVAILABLE
                if "errors" in data:
                    for error in data["errors"]:
                        if error.get("title") == "Not Found Error":
                            results[error.get("value", "").lower()] = 0  # AVAILABLE
                
                # Log available usernames to file
                available = [name for name, status in results.items() if status == 0]
                if available:
                    await TwitterXAPIChecker.log_available_usernames(available)
                
                # Fill in missing usernames (timeouts/errors)
                for username in usernames:
                    if username.lower() not in results:
                        results[username.lower()] = None
                
                return results
            
            elif response.status_code == 429:
                # Rate limited by X API
                return {username: None for username in usernames}
            
            else:
                return {username: None for username in usernames}
        
        except Exception as e:
            return {username: None for username in usernames}
    
    @staticmethod
    async def log_available_usernames(available_usernames: List[str], filename: str = "available_usernames.txt"):
        """Log found available usernames to file"""
        try:
            def write_to_file():
                with open(filename, "a") as f:
                    for username in available_usernames:
                        f.write(f"{username}\n")
            
            await asyncio.to_thread(write_to_file)
        except Exception as e:
            pass


class PatternSelect(discord.ui.Select):
    def __init__(self):
        patterns = [
            discord.SelectOption(label="4-Letter Pattern", description="4 random letters (e.g., zetre)", value="1"),
            discord.SelectOption(label="5-Letter Pattern", description="5 random letters (e.g., treui)", value="2"),
            discord.SelectOption(label="4-Char Mixed", description="4 chars with numbers (e.g., 8AUT)", value="3"),
            discord.SelectOption(label="5-Char Mixed", description="5 chars with numbers (e.g., T23U)", value="4"),
            discord.SelectOption(label="Custom Pattern", description="Enter your own L&D pattern", value="8"),
            discord.SelectOption(label="Load from File", description="Upload a .txt file", value="9"),
        ]
        super().__init__(placeholder="Select a pattern...", min_values=1, max_values=1, options=patterns)

    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_sessions[user_id]["pattern_choice"] = self.values[0]
        
        if self.values[0] == "8":
            await interaction.response.send_message(
                "📝 Enter your custom pattern using:\n- **L** for letters\n- **D** for digits\n- **S** for symbols (_.-)\nExample: `LL.DD` or `L_DLD`",
                ephemeral=True
            )
        elif self.values[0] == "9":
            await interaction.response.send_message(
                "📄 Upload a .txt file with usernames (one per line)",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"✅ Pattern selected: `{self.values[0]}`\n\n**How many usernames to generate?**",
                ephemeral=True,
                view=QuantityView()
            )


class PlatformSelect(discord.ui.Select):
    def __init__(self):
        platforms = [
            discord.SelectOption(label="Roblox", value="1"),
            discord.SelectOption(label="Twitter/X", value="2"),
            discord.SelectOption(label="GitHub", value="3"),
            discord.SelectOption(label="TikTok", value="4"),
            discord.SelectOption(label="Discord", value="5"),
            discord.SelectOption(label="All Platforms", value="6"),
        ]
        super().__init__(placeholder="Select platform(s)...", min_values=1, max_values=1, options=platforms)

    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_sessions[user_id]["platforms"] = self.values
        
        platform_names = {
            "1": "Roblox",
            "2": "Twitter/X",
            "3": "GitHub",
            "4": "TikTok",
            "5": "Discord",
            "6": "All Platforms"
        }
        
        selected = [platform_names[p] for p in self.values if p != "6"] or ["All Platforms"]
        
        # Now show pattern selection
        view = discord.ui.View()
        view.add_item(PatternSelect())
        
        await interaction.response.send_message(
            f"✅ Platforms selected: {', '.join(selected)}\n\n**Select a username pattern:**",
            ephemeral=True,
            view=view
        )


class QuantityView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Enter Custom Amount", style=discord.ButtonStyle.success)
    async def qty_custom(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = CustomQuantityModal()
        await interaction.response.send_modal(modal)


class CustomQuantityModal(discord.ui.Modal, title="Custom Quantity"):
    quantity = discord.ui.TextInput(label="Number of usernames", placeholder="Enter number", min_length=1, max_length=5)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            qty = int(self.quantity.value)
            user_id = interaction.user.id
            member = interaction.guild.get_member(user_id) if interaction.guild else None
            
            # Check if this is a VIP user doing a regular hunt
            hunt_type = user_sessions.get(user_id, {}).get("hunt_type", "username")
            is_vip = is_vip_user(user_id, member)
            
            allowed, message, max_qty = can_hunt(user_id, "username", member)
            if not allowed:
                await interaction.response.send_message(f"❌ {message}", ephemeral=True)
                return

            if qty < 1 or qty > max_qty:
                permission_tier = get_user_permission_tier(user_id, member)
                tier_name = {"owner": "Owner", "whitelisted": "VIP", "normal": "Normal"}.get(permission_tier, "User")
                await interaction.response.send_message(
                    f"❌ Please enter a number between 1 and {max_qty:,}\n💡 **{tier_name} users** can hunt up to **{max_qty:,}** usernames at a time",
                    ephemeral=True
                )
                return
            
            user_sessions[user_id]["quantity"] = qty
            user_sessions[user_id]["hunt_type"] = "username"
            
            await interaction.response.send_message(f"✅ Set to {qty:,} usernames\n\n**Ready to start checking!**", view=StartCheckingView(), ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Invalid number", ephemeral=True)


class StartCheckingView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Start Checking", style=discord.ButtonStyle.success)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        user_id = interaction.user.id
        
        if user_id not in user_sessions:
            await interaction.followup.send("❌ Session not found. Please start over.", ephemeral=True)
            return
        
        session = user_sessions[user_id]
        await check_usernames(interaction, session)


class ExportView(discord.ui.View):
    def __init__(self, session_data):
        super().__init__()
        self.session_data = session_data

    @discord.ui.button(label="All Valid", style=discord.ButtonStyle.success)
    async def export_all_valid(self, interaction: discord.Interaction, button: discord.ui.Button):
        results = self.session_data.get("results", {})
        valid_list = []
        
        for username, status_dict in results.items():
            for platform, status in status_dict.items():
                if status == 0:
                    valid_list.append(f"{username} ({platform})")
        
        if valid_list:
            text = "\n".join(valid_list)
            await send_as_file(interaction, text, "valid_usernames.txt")
        else:
            await interaction.response.send_message("❌ No valid usernames found", ephemeral=True)

    @discord.ui.button(label="By Platform", style=discord.ButtonStyle.primary)
    async def export_by_platform(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Select a platform:", view=PlatformFilterView(self.session_data), ephemeral=True)

    @discord.ui.button(label="All Results", style=discord.ButtonStyle.secondary)
    async def export_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        results = self.session_data.get("results", {})
        text_lines = []
        
        for username, status_dict in results.items():
            for platform, status in status_dict.items():
                status_name = {0: "VALID", 1: "TAKEN", 2: "CENSORED"}.get(status, "ERROR")
                text_lines.append(f"{username} - {platform}: {status_name}")
        
        if text_lines:
            text = "\n".join(text_lines)
            await send_as_file(interaction, text, "all_results.txt")
        else:
            await interaction.response.send_message("❌ No results found", ephemeral=True)


class PlatformFilterView(discord.ui.View):
    def __init__(self, session_data):
        super().__init__()
        self.session_data = session_data

    @discord.ui.select(placeholder="Choose platform...", options=[
        discord.SelectOption(label="Roblox", value="Roblox"),
        discord.SelectOption(label="Twitter/X", value="Twitter/X"),
        discord.SelectOption(label="GitHub", value="GitHub"),
        discord.SelectOption(label="TikTok", value="TikTok"),
        discord.SelectOption(label="Discord", value="Discord"),
    ])
    async def select_platform(self, interaction: discord.Interaction, select: discord.ui.Select):
        platform = select.values[0]
        results = self.session_data.get("results", {})
        
        valid_list = []
        for username, status_dict in results.items():
            if platform in status_dict and status_dict[platform] == 0:
                valid_list.append(username)
        
        if valid_list:
            text = "\n".join(valid_list)
            await send_as_file(interaction, text, f"valid_{platform.lower()}.txt")
        else:
            await interaction.response.send_message(f"❌ No valid usernames for {platform}", ephemeral=True)


async def send_as_file(interaction: discord.Interaction, content: str, filename: str):
    """Send text content as a Discord file"""
    file = discord.File(fp=io.BytesIO(content.encode()), filename=filename)
    await interaction.response.send_message(f"📥 Downloading {filename}...", file=file, ephemeral=True)


async def followup_send_file(interaction: discord.Interaction, content: str, filename: str, mention_user: Optional[discord.User] = None):
    """Send file content via a follow-up message, optionally pinging the user"""
    file = discord.File(fp=io.BytesIO(content.encode()), filename=filename)
    mention_text = mention_user.mention if mention_user else "Here are the results"
    await interaction.followup.send(f"{mention_text} Here's your username list:", file=file)


async def check_usernames(interaction: discord.Interaction, session: Dict):
    """Main username checking function"""
    user_id = interaction.user.id
    
    try:
        # Generate usernames
        pattern = session["pattern_choice"]
        quantity = session.get("quantity", 100)
        
        pattern_generators = {
            "1": lambda: ''.join(random.choices(string.ascii_uppercase, k=4)),  # 4-Letter pattern
            "2": lambda: ''.join(random.choices(string.ascii_uppercase, k=5)),  # 5-Letter pattern
            "3": lambda: UsernameChecker.gen_mixed_4(),  # 4-Char mixed (numbers+letters)
            "4": lambda: UsernameChecker.gen_mixed_5(),  # 5-Char mixed (numbers+letters)
        }
        
        gen_fn = pattern_generators.get(pattern, UsernameChecker.gen_pat_digit)
        usernames = [gen_fn() for _ in range(quantity)]
        
        # Platform mappings (Roblox only)
        platform_map = {
            "1": ("Roblox", UsernameChecker.chk_roblox),
        }
        
        platforms_to_check = session.get("platforms", ["1"])

        
        # Initialize results
        results = {name: {} for name in usernames}
        valid_count = 0
        total_checks = 0
        
        # Embed for progress
        progress_embed = discord.Embed(
            title="🔍 Checking Usernames...",
            description=f"Checking {len(usernames)} usernames across {len(platforms_to_check)} platform(s)",
            color=discord.Color.blue()
        )
        progress_msg = await interaction.followup.send(embed=progress_embed, ephemeral=True)
        
        # Check usernames
        for i, username in enumerate(usernames):
            for platform_key in platforms_to_check:
                if platform_key not in platform_map:
                    continue
                
                platform_name, check_fn = platform_map[platform_key]
                
                # Pass user_id for Twitter rate limiting
                if platform_key == "2":  # Twitter/X
                    code = await check_fn(username, user_id)
                else:
                    code = await check_fn(username)
                
                results[username][platform_name] = code
                total_checks += 1
                
                if code == 0:
                    valid_count += 1
            
            # Update progress on every username with animation
            progress_percent = int((i + 1) / len(usernames) * 100)
            progress_bar = PROGRESS_FULL * int(progress_percent / 10) + PROGRESS_EMPTY * (10 - int(progress_percent / 10))
            
            progress_embed = discord.Embed(
                title="🔍 Checking Usernames...",
                color=discord.Color.blue()
            )
            progress_embed.add_field(
                name="Progress",
                value=f"```{progress_bar}``` {progress_percent}%",
                inline=False
            )
            progress_embed.add_field(
                name="Status",
                value=f"✅ Checked: `{i + 1}/{len(usernames)}` | 💎 Valid: `{valid_count}`",
                inline=False
            )
            
            try:
                await progress_msg.edit(embed=progress_embed)
            except:
                pass
            
            # Rate limiting - small delay to avoid API throttling
            await asyncio.sleep(0.05)
        
        # Remove user from concurrent Twitter users when done
        if user_id in TWITTER_CONCURRENT_USERS:
            TWITTER_CONCURRENT_USERS.discard(user_id)
        
        # Store results
        user_sessions[user_id]["results"] = results
        
        # Send results summary
        success_rate = (valid_count/total_checks*100) if total_checks > 0 else 0
        
        # Create a visual success rate bar
        rate_bar = PROGRESS_FULL * int(success_rate / 10) + PROGRESS_EMPTY * (10 - int(success_rate / 10))
        
        summary_embed = discord.Embed(
            title="✅ Checking Complete!",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        
        # Add stats with visual formatting
        summary_embed.add_field(
            name="📊 Statistics",
            value=f"**Total Checked:** `{total_checks}`\n**Valid Found:** `{valid_count}`\n**Taken:** `{total_checks - valid_count}`",
            inline=False
        )
        
        summary_embed.add_field(
            name="📈 Success Rate",
            value=f"```{rate_bar}``` `{success_rate:.1f}%`",
            inline=False
        )
        
        summary_embed.add_field(
            name="⏱️ Platforms Checked",
            value=f"`{len(platforms_to_check)}` platform(s)",
            inline=True
        )
        
        summary_embed.add_field(
            name="🎯 Pattern Used",
            value=f"`Pattern {pattern}`",
            inline=True
        )
        
        summary_embed.set_footer(text=f"Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Extract valid usernames and save to server
        valid_usernames = []
        for username, status_dict in results.items():
            for platform, status in status_dict.items():
                if status == 0:  # Valid
                    valid_usernames.append(username)
                    break  # Add each username only once
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Save valid usernames to file on server
        if valid_usernames:
            await save_valid_usernames_to_server(valid_usernames, user_id, pattern, timestamp)
        
        # Prepare completion message with export options
        completion_msg = await interaction.followup.send(embed=summary_embed, view=ExportView(user_sessions[user_id]), ephemeral=False)
        
        # Ping user with completion notification
        user = interaction.user
        if valid_usernames:
            pattern_label = pattern or "custom"
            file_content = "\n".join(valid_usernames)
            filename = f"valid_{user_id}_{pattern_label}_{timestamp}.txt"
            await followup_send_file(interaction, file_content, filename, mention_user=user)
        if valid_usernames:
            ping_embed = discord.Embed(
                title="🎉 Hunt Complete!",
                description=f"**{user.mention}** - Your username hunt is complete!\n\n✅ **Found {valid_count} valid username(s)**",
                color=discord.Color.gold()
            )
            ping_embed.add_field(
                name="📝 Valid Usernames",
                value=f"```{', '.join(valid_usernames[:10])}{'...' if len(valid_usernames) > 10 else ''}```",
                inline=False
            )
            await interaction.followup.send(embed=ping_embed, ephemeral=False)
        else:
            no_valid_embed = discord.Embed(
                title="❌ No Valid Usernames",
                description=f"**{user.mention}** - Hunt completed but no available usernames were found.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=no_valid_embed, ephemeral=False)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)


async def save_valid_usernames_to_server(usernames: List[str], user_id: int, pattern: Optional[str], timestamp: Optional[str] = None):
    """Save valid usernames to a file on the server"""
    try:
        # Create results directory if it doesn't exist
        results_dir = Path("hunt_results")
        results_dir.mkdir(exist_ok=True)
        
        # Create filename with timestamp and user ID
        timestamp = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
        pattern_label = pattern or "custom"
        filename = results_dir / f"valid_{user_id}_{pattern_label}_{timestamp}.txt"
        
        # Write usernames to file
        def write_file():
            with open(filename, "w") as f:
                for username in usernames:
                    f.write(f"{username}\n")
        
        await asyncio.to_thread(write_file)
        
    except Exception as e:
        pass  # Silently fail - doesn't affect hunt result


@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")


@bot.tree.command(name="socialhunt", description="Check 10 random 4-letter usernames on Instagram, TikTok, Twitter, and YouTube (with proxies)")
async def socialhunt(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=False)
    usernames = ["".join(random.choices(string.ascii_lowercase, k=4)) for _ in range(10)]
    all_hits = []
    results = {}
    proxies = load_proxies()
    burned_proxies = set()
    session = requests.Session()
    for uname in usernames:
        uname_result = {}
        all_available = True
        for platform, url_pattern in SOCIAL_PLATFORMS.items():
            url = url_pattern.format(uname)
            attempt = 0
            max_attempts = len(proxies) if proxies else 1
            while attempt < max_attempts:
                proxy_ip = random.choice(proxies) if proxies else None
                if proxy_ip in burned_proxies:
                    attempt += 1
                    continue
                proxy_dict = get_proxy_dict(proxy_ip) if proxy_ip else None
                try:
                    resp = await asyncio.to_thread(
                        session.get, url,
                        headers=SOCIAL_HEADERS,
                        proxies=proxy_dict,
                        timeout=8
                    )
                    if resp.status_code == 404:
                        uname_result[platform] = ("AVAILABLE", url)
                        break
                    elif resp.status_code == 200:
                        uname_result[platform] = ("TAKEN", url)
                        all_available = False
                        break
                    elif resp.status_code == 429:
                        burned_proxies.add(proxy_ip)
                        attempt += 1
                        continue
                    elif resp.status_code == 403:
                        uname_result[platform] = ("BLOCKED", url)
                        all_available = False
                        break
                    else:
                        uname_result[platform] = (f"UNKNOWN:{resp.status_code}", url)
                        all_available = False
                        break
                except Exception as e:
                    burned_proxies.add(proxy_ip)
                    attempt += 1
                    if attempt >= max_attempts:
                        uname_result[platform] = ("ERROR", str(e))
                        all_available = False
                finally:
                    await asyncio.sleep(random.uniform(SOCIALHUNT_MIN_DELAY, SOCIALHUNT_MAX_DELAY))
        results[uname] = uname_result
        if all_available:
            all_hits.append(uname)
            with open("hits.txt", "a") as f:
                f.write(uname + "\n")

    embed = discord.Embed(
        title="🌈 Social Username Checker Results (Proxy Mode)",
        description="10 random 4-letter usernames checked across Instagram, TikTok, Twitter, and YouTube.",
        color=discord.Color.blurple()
    )
    for idx, (uname, uname_result) in enumerate(results.items()):
        value_lines = []
        for platform, (status, url) in uname_result.items():
            if status == "AVAILABLE":
                emoji = "🟢"
            elif status == "TAKEN":
                emoji = "🔴"
            elif status == "BLOCKED":
                emoji = "🟡"
            elif status.startswith("UNKNOWN"):
                emoji = "⚪"
            else:
                emoji = "⚠️"
            value_lines.append(f"{emoji} **{platform}**: `{status}`")
        embed.add_field(
            name=f"`{uname}`",
            value="\n".join(value_lines),
            inline=False
        )
    if all_hits:
        embed.add_field(
            name="🎉 All-Platform Hits",
            value=", ".join(all_hits) + "\n(Saved to hits.txt)",
            inline=False
        )
    embed.set_footer(text=f"v{BOT_VERSION} | RGB UI | Proxy Support | {len(results)} usernames checked")
    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="snipe", description="Start checking usernames across platforms")
async def snipe_command(interaction: discord.Interaction):
    """Start the username sniping process"""
    
    # Check if channel restriction is enabled
    if ALLOWED_CHANNEL_IDS:
        if interaction.channel_id not in ALLOWED_CHANNEL_IDS:
            channels_list = ", ".join([f"<#{cid}>" for cid in ALLOWED_CHANNEL_IDS])
            await interaction.response.send_message(
                f"❌ This command can only be used in: {channels_list}",
                ephemeral=True
            )
            return
    
    user_id = interaction.user.id
    member = interaction.guild.get_member(user_id) if interaction.guild else None
    
    # Check if user is VIP
    is_vip = is_vip_user(user_id, member)
    
    if is_vip:
        # VIP user - check VIP permissions
        # VIPs have unlimited access to text hunts and 10k per 3 days for regular hunts
        permission_tier = get_user_permission_tier(user_id, member)
        tier_name = {"owner": "Owner", "whitelisted": "VIP 🌟"}.get(permission_tier, "VIP")
        
        # Initialize session
        user_sessions[user_id] = {
            "pattern_choice": None,
            "quantity": 100,
            "platforms": [],
            "results": {},
            "is_vip": True
        }
        
        # Create platform select view
        view = discord.ui.View()
        view.add_item(PlatformSelect())
        
        # Beautiful VIP Embed
        embed = discord.Embed(
            title="✨ VIP Username Sniper - Premium Access ✨",
            description="Welcome to the **Premium Hunting Experience**!\n\n**Select platform(s) to check** 👇",
            color=discord.Color.from_rgb(255, 215, 0)  # Gold color for VIP
        )
        embed.add_field(
            name="⭐ VIP Exclusive Features",
            value="✓ **Text Hunts**: Unlimited 500-letter custom hunts\n✓ **Regular Hunts**: 10,000 per 3 days\n✓ **Priority Processing**: Get results faster\n✓ **Advanced Patterns**: All patterns available",
            inline=False
        )
        embed.add_field(
            name="🎯 Hunt Types Available",
            value="**Text Hunt** (Small Letters)\n↳ Unlimited custom 500-letter hunts for Roblox\n\n**Regular Hunt**\n↳ 10,000 hunts per 3 days",
            inline=False
        )
        embed.add_field(
            name="👑 Your Status",
            value=f"**{tier_name}** Member\n🌟 Premium Access Active\n⚡ No Daily Limits on Text Hunts",
            inline=False
        )
        embed.add_field(
            name="📌 Version",
            value=f"`v{BOT_VERSION}` ({BOT_VERSION_DATE})",
            inline=True
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1995/1995467.png")
        embed.set_footer(text=f"VIP Premium Username Sniper v{BOT_VERSION} | Your hunting power is limitless!")
        
        # Add a stylized border effect with zero-width spaces (visual enhancement)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    else:
        # Regular user - standard experience
        allowed, message, max_qty = can_hunt(user_id, "username", member)
        
        permission_tier = get_user_permission_tier(user_id, member)
        tier_name = {"normal": "Normal"}.get(permission_tier, "User")
        
        if not allowed:
            await interaction.response.send_message(f"❌ {message}", ephemeral=True)
            return
        
        # Initialize session
        user_sessions[user_id] = {
            "pattern_choice": None,
            "quantity": 100,
            "platforms": [],
            "results": {},
            "is_vip": False
        }
        
        # Create platform select view FIRST
        view = discord.ui.View()
        view.add_item(PlatformSelect())
        
        # Standard embed for regular users
        embed = discord.Embed(
            title="🎯 Username Sniper Bot",
            description="Welcome to **Custom Renro's** Python Roblox Username Sniper!\n\n**Select platform(s) to check** 👇",
            color=discord.Color.from_rgb(255, 69, 0)
        )
        embed.add_field(
            name="⚡ Features",
            value="✓ Multi-platform checking\n✓ Custom patterns\n✓ Real-time progress\n✓ Export results",
            inline=False
        )
        embed.add_field(
            name="📌 Version",
            value=f"`v{BOT_VERSION}` ({BOT_VERSION_DATE})",
            inline=True
        )
        embed.add_field(
            name="👤 Your Tier",
            value=f"`{tier_name}` - Max: **{max_qty:,}** hunts/week",
            inline=True
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1995/1995467.png")
        embed.set_footer(text=f"Multi-platform username availability checker v{BOT_VERSION}")
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


@bot.tree.command(name="help", description="Show help information")
async def help_command(interaction: discord.Interaction):
    """Show help"""
    user_id = interaction.user.id
    member = interaction.guild.get_member(user_id) if interaction.guild else None
    is_vip = is_vip_user(user_id, member)
    permission_tier = get_user_permission_tier(user_id, member)
    tier_name = {"owner": "VIP 🌟", "whitelisted": "VIP 🌟", "normal": "Normal"}.get(permission_tier, "User")
    
    if is_vip:
        # VIP Help Embed
        embed = discord.Embed(
            title="✨ VIP Help - Premium Username Sniper ✨",
            color=discord.Color.from_rgb(255, 215, 0),
            description="You have access to exclusive VIP features!"
        )
        embed.add_field(
            name="How to Use",
            value="""
1. Run `/snipe` to start
2. Choose **Text Hunt** or **Regular Hunt**
3. Select a username pattern
4. Enter quantity (based on hunt type)
5. Select platforms to check
6. Click "Start Checking"
7. Export results in various formats
            """,
            inline=False
        )
        embed.add_field(
            name="🌟 VIP Hunt Limits",
            value=f"""
**Text Hunts** (Small Letters for Roblox)
↳ **Unlimited** 500-letter custom hunts 🔓
↳ Perfect for Roblox username hunting
↳ No daily/weekly limits!

**Regular Hunts**
↳ **10,000 hunts per 3 days**
↳ Full access to all platforms
↳ Advanced pattern selection

**Your Status**: `{tier_name}` ⭐
            """,
            inline=False
        )
        embed.add_field(
            name="Patterns Available",
            value="""
- **X_XXX**: Letter_3Letters (e.g., A_BCD)
- **XX_XX**: 2Letters_2Letters (e.g., AB_CD)
- **XXX_X**: 3Letters_Letter (e.g., ABC_D)
- **1_X2X**: Digit_Letter+Digit+Letter
- **1X_2X**: Digit+Letter_Digit+Letter
- **1X2_X**: Digit+Letter+Digit_Letter
- **X1X2X**: Mixed with strict rules
- **Custom**: Define your own with L (letter) and D (digit)
            """,
            inline=False
        )
        embed.add_field(
            name="Export Options",
            value="""
- **All Valid**: Export all available usernames
- **By Platform**: Filter by specific platform
- **All Results**: Complete results with status for each
            """,
            inline=False
        )
        embed.add_field(
            name="🎁 VIP Perks",
            value="⭐ Unlimited text hunts\n⭐ Priority processing\n⭐ 10k hunts per 3 days\n⭐ All patterns unlocked",
            inline=True
        )
        embed.add_field(
            name="Version",
            value=f"v{BOT_VERSION} ({BOT_VERSION_DATE})",
            inline=True
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1995/1995467.png")
        embed.set_footer(text="VIP Premium Features - Enjoy your exclusive access!")
        
    else:
        # Regular user help
        max_qty = HUNT_LIMITS[permission_tier]
        
        embed = discord.Embed(
            title="📖 Help - Username Sniper Bot",
            color=discord.Color.gold()
        )
        embed.add_field(
            name="How to Use",
            value="""
1. Run `/snipe` to start
2. Select a username pattern
3. Enter quantity (or choose preset)
4. Select platforms to check
5. Click "Start Checking"
6. Export results in various formats
            """,
            inline=False
        )
        embed.add_field(
            name="📊 Hunt Limits (Weekly Reset)",
            value=f"""
👑 **Owner**: 50,000 hunts/week
⭐ **VIP**: Unlimited text hunts + 10,000 regular hunts per 3 days
👤 **Normal**: 10,000 hunts/week (sniper) / 1,000 hunts/week (normal)

**Your Tier**: `{tier_name}` - **{max_qty:,}** hunts/week
            """,
            inline=False
        )
        embed.add_field(
            name="Patterns",
            value="""
- **X_XXX**: Letter_3Letters (e.g., A_BCD)
- **XX_XX**: 2Letters_2Letters (e.g., AB_CD)
- **XXX_X**: 3Letters_Letter (e.g., ABC_D)
- **1_X2X**: Digit_Letter+Digit+Letter
- **1X_2X**: Digit+Letter_Digit+Letter
- **1X2_X**: Digit+Letter+Digit_Letter
- **X1X2X**: Mixed with strict rules
- **Custom**: Define your own with L (letter) and D (digit)
            """,
            inline=False
        )
        embed.add_field(
            name="Export Options",
            value="""
- **All Valid**: Export all available usernames
- **By Platform**: Filter by specific platform
- **All Results**: Complete results with status for each
            """,
            inline=False
        )
        embed.add_field(
            name="Want VIP Access?",
            value="Contact the bot owner to become a VIP member and unlock unlimited text hunts!",
            inline=False
        )
        embed.add_field(
            name="Version",
            value=f"v{BOT_VERSION} ({BOT_VERSION_DATE})",
            inline=True
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)


# ==================== REVERSE USERNAME SEARCH (SnipeLarge) ====================

class ReverseUsernameSearcher:
    """Check where a specific username exists across all social media platforms"""
    
    def __init__(self):
        self.platforms = self._load_socials()
        self.request_tracking = {}  # {user_id: {"requests": [], "last_request": datetime}}
        self.REQUESTS_PER_5_SEC = 1
        self.MAX_REQUESTS_PER_HUNT = 100
        self.RATE_LIMIT_SECONDS = 5
    
    def _load_socials(self) -> Dict[str, Tuple[str, str]]:
        """Load social media platforms from socials.txt"""
        platforms = {}
        
        # Try multiple paths for socials.txt (handles different working directories)
        possible_paths = [
            'socials.txt',
            './socials.txt',
            '/home/container/socials.txt',
            os.path.join(os.path.dirname(__file__), 'socials.txt'),
            os.path.join(os.getcwd(), 'socials.txt')
        ]
        
        socials_file = None
        for path in possible_paths:
            if os.path.exists(path):
                socials_file = path
                break
        
        if not socials_file:
            print(f"⚠️  socials.txt not found. Checked paths: {possible_paths}")
            return platforms
        
        try:
            with open(socials_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            social, page = line.split(':', 1)
                            if '<user>' in page:
                                prefix, suffix = page.split('<user>')
                                platforms[social.strip()] = (prefix, suffix)
                        except ValueError:
                            continue
        except FileNotFoundError:
            print(f"⚠️  Could not open {socials_file}")
        
        return platforms
    
    def _check_rate_limit(self, user_id: int) -> Tuple[bool, str]:
        """Check if user can make another request"""
        now = datetime.now()
        
        if user_id not in self.request_tracking:
            self.request_tracking[user_id] = {"requests": [], "last_request": now}
            return True, "✅"
        
        # Remove requests older than 5 seconds
        tracking = self.request_tracking[user_id]
        tracking["requests"] = [req_time for req_time in tracking["requests"] 
                               if (now - req_time).total_seconds() < self.RATE_LIMIT_SECONDS]
        
        # Check if at max requests
        if len(tracking["requests"]) >= self.MAX_REQUESTS_PER_HUNT:
            return False, f"❌ Max {self.MAX_REQUESTS_PER_HUNT} requests reached for this hunt"
        
        # Check if enough time has passed since last request
        time_since_last = (now - tracking["last_request"]).total_seconds()
        if time_since_last < self.RATE_LIMIT_SECONDS:
            wait_time = self.RATE_LIMIT_SECONDS - time_since_last
            return False, f"⏳ Wait {wait_time:.1f}s before next request (1 request per 5 seconds)"
        
        return True, "✅"
    
    def _record_request(self, user_id: int):
        """Record a request for rate limiting"""
        now = datetime.now()
        if user_id not in self.request_tracking:
            self.request_tracking[user_id] = {"requests": [], "last_request": now}
        
        self.request_tracking[user_id]["requests"].append(now)
        self.request_tracking[user_id]["last_request"] = now
    
    async def search_username(self, username: str, user_id: int) -> Dict[str, str]:
        """Search for username across all platforms"""
        results = {}
        
        for platform, (prefix, suffix) in self.platforms.items():
            # Check rate limit before each request
            allowed, message = self._check_rate_limit(user_id)
            if not allowed:
                results[platform] = f"⏳ Rate limited"
                continue
            
            try:
                url = f"{prefix.strip()}{username.strip()}{suffix.strip()}"
                response = await asyncio.to_thread(requests.get, url, timeout=10)
                self._record_request(user_id)
                
                if response.status_code == 200:
                    results[platform] = "✅ AVAILABLE"
                else:
                    results[platform] = "❌ TAKEN"
                
                # Rate limit: 1 request per 5 seconds
                await asyncio.sleep(5)
            except Exception as e:
                results[platform] = "⚠️  ERROR"
        
        return results

# Initialize reverse search
reverse_searcher = ReverseUsernameSearcher()


@bot.tree.command(name="snipelarge", description="🔍 Search where a specific username exists across all platforms")
@app_commands.describe(username="The username to search for")
async def snipelarge(interaction: discord.Interaction, username: str):
    """Reverse search: Find where a specific username exists"""
    
    # Check if allowed in channel
    if ALLOWED_CHANNEL_IDS and interaction.channel_id not in ALLOWED_CHANNEL_IDS:
        await interaction.response.send_message(
            "❌ This command is not allowed in this channel.",
            ephemeral=True
        )
        return
    
    # Validate username
    if len(username) < 2 or len(username) > 50:
        await interaction.response.send_message(
            "❌ Username must be between 2 and 50 characters",
            ephemeral=True
        )
        return
    
    # Initial response
    await interaction.response.defer()
    
    # Create progress embed
    progress_embed = discord.Embed(
        title=f"🔍 Searching: '{username}'",
        description="Checking availability across platforms...",
        color=discord.Color.gold()
    )
    progress_embed.set_footer(text="Rate limit: 1 request per 5 seconds")
    
    progress_msg = await interaction.followup.send(embed=progress_embed)
    
    # Perform search
    results = await reverse_searcher.search_username(username, interaction.user.id)
    
    # Create results embed
    results_embed = discord.Embed(
        title=f"📊 Search Results for: '{username}'",
        color=discord.Color.green(),
        timestamp=datetime.now()
    )
    
    available_count = sum(1 for v in results.values() if "AVAILABLE" in v)
    taken_count = sum(1 for v in results.values() if "TAKEN" in v)
    
    # Add results
    available_platforms = []
    taken_platforms = []
    
    for platform, status in sorted(results.items()):
        if "AVAILABLE" in status:
            available_platforms.append(f"✅ {platform}")
        elif "TAKEN" in status:
            taken_platforms.append(f"❌ {platform}")
    
    if available_platforms:
        results_embed.add_field(
            name="✅ AVAILABLE",
            value="\n".join(available_platforms) or "None",
            inline=False
        )
    
    if taken_platforms:
        results_embed.add_field(
            name="❌ TAKEN",
            value="\n".join(taken_platforms) or "None",
            inline=False
        )
    
    results_embed.add_field(
        name="📈 Summary",
        value=f"Available: **{available_count}** | Taken: **{taken_count}** | Total: **{len(results)}**",
        inline=False
    )
    
    # Save results to file
    filename = f"search_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    try:
        with open(filename, 'w') as f:
            f.write(f"Username Search Results\n")
            f.write(f"Username: {username}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"User: {interaction.user} ({interaction.user.id})\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("AVAILABLE:\n")
            for platform, status in sorted(results.items()):
                if "AVAILABLE" in status:
                    prefix, suffix = reverse_searcher.platforms.get(platform, ("", ""))
                    url = f"{prefix}{username}{suffix}"
                    f.write(f"✅ {platform}: {url}\n")
            
            f.write("\nTAKEN:\n")
            for platform, status in sorted(results.items()):
                if "TAKEN" in status:
                    prefix, suffix = reverse_searcher.platforms.get(platform, ("", ""))
                    url = f"{prefix}{username}{suffix}"
                    f.write(f"❌ {platform}: {url}\n")
            
            f.write("\nERRORS:\n")
            for platform, status in sorted(results.items()):
                if "ERROR" in status or "Rate" in status:
                    f.write(f"⚠️  {platform}: {status}\n")
        
        results_embed.add_field(
            name="📁 Results Saved",
            value=f"`{filename}`",
            inline=False
        )
    except Exception as e:
        results_embed.add_field(
            name="⚠️  File Save Error",
            value=f"Could not save results: {str(e)}",
            inline=False
        )
    
    # Update progress message with results
    await progress_msg.edit(embed=results_embed)


# Run the bot
if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    
    # If not in environment, try .env file
    if not TOKEN:
        load_dotenv()
        TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    
    # If still not found, check if .env file exists
    if not TOKEN:
        env_path = Path(".env")
        if not env_path.exists():
            # Create from template if it exists
            if Path(".env.example").exists():
                import shutil
                try:
                    shutil.copy(".env.example", ".env")
                    print("⚠️  .env file created from template")
                except:
                    pass
        
        # Try loading again
        load_dotenv()
        TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    
    if not TOKEN or TOKEN == "your_bot_token_here":
        print("❌ Error: DISCORD_BOT_TOKEN not found or invalid")
        print("📝 Instructions:")
        print("   Option 1 - Set environment variable:")
        print("     export DISCORD_BOT_TOKEN='your_token_here'")
        print("   Option 2 - Edit .env file:")
        print("     nano .env")
        print("     Replace 'your_bot_token_here' with your actual token")
        print("   Option 3 - Pterodactyl startup parameter:")
        print("     Set DISCORD_BOT_TOKEN in server startup variables")
        exit(1)
    
    print(f"✅ Bot version {BOT_VERSION} starting...")
    print(f"✅ Bot token loaded (length: {len(TOKEN)} characters)")
    if BOT_OWNER_ID:
        print(f"✅ Bot owner ID: {BOT_OWNER_ID}")
    if WHITELISTED_USERS:
        print(f"✨ VIP Users ({len(WHITELISTED_USERS)}): {', '.join(str(uid) for uid in WHITELISTED_USERS)}")
        print(f"✨ VIP Features Active: Unlimited Text Hunts + 10,000 per 3 days")
    if X_BEARER_TOKEN:
        print(f"🔌 X API v2 Integration: ENABLED (Official batch checking)")
        print(f"📊 VIP Twitter Limit: 100 requests/hour (batch mode)")
    else:
        print(f"⚠️  X API v2 Token not configured (batch Twitter checking disabled)")
    bot.run(TOKEN)

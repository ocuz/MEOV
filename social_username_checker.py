import requests
import random
import string
import time
from typing import Dict

# Color output for terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

# Modern User-Agent header
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

PLATFORMS = {
    "Instagram": "https://www.instagram.com/{}/",
    "TikTok": "https://www.tiktok.com/@{}",
    "Twitter": "https://www.twitter.com/{}/",
    "YouTube": "https://www.youtube.com/user/{}"
}

# Generate 10 random 4-letter usernames
usernames = ["".join(random.choices(string.ascii_lowercase, k=4)) for _ in range(10)]

all_platform_hits = []

for username in usernames:
    status: Dict[str, str] = {}
    print(f"\nChecking username: {username}")
    all_available = True
    for platform, url_pattern in PLATFORMS.items():
        url = url_pattern.format(username)
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 404:
                print(f"  {Colors.GREEN}[AVAILABLE]{Colors.RESET} {platform}: {url}")
                status[platform] = "available"
            elif resp.status_code == 200:
                print(f"  {Colors.RED}[TAKEN]{Colors.RESET} {platform}: {url}")
                status[platform] = "taken"
                all_available = False
            elif resp.status_code in (403, 429):
                print(f"  {Colors.YELLOW}[BLOCKED/RATE-LIMIT]{Colors.RESET} {platform}: {url}")
                status[platform] = "blocked"
                all_available = False
            else:
                print(f"  [UNKNOWN {resp.status_code}] {platform}: {url}")
                status[platform] = f"unknown:{resp.status_code}"
                all_available = False
        except Exception as e:
            print(f"  {Colors.YELLOW}[ERROR]{Colors.RESET} {platform}: {e}")
            status[platform] = "error"
            all_available = False
        time.sleep(random.uniform(1.5, 3.0))
    if all_available:
        all_platform_hits.append(username)
        with open("hits.txt", "a") as f:
            f.write(username + "\n")
        print(f"{Colors.GREEN}>> {username} is available on ALL platforms! Saved to hits.txt{Colors.RESET}")

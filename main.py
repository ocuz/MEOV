import random
import string
import requests
import os
from colorama import Fore, Style, init

init(autoreset=True)

ASCII_BANNER = r"""
.___  ___.  _______   ______   ____    ____ 
|   \/   | |   ____| /  __  \  \   \  /   / 
|  \  /  | |  |__   |  |  |  |  \   \/   /  
|  |\/|  | |   __|  |  |  |  |   \      /   
|  |  |  | |  |____ |  `--'  |    \    /    
|__|  |__| |_______| \______/      \__/     
                                             
"""

print(ASCII_BANNER)
print("Credits to ocuz (Clemouche) :)\n")

print("Choose a pattern:\n")

def gen_pat_digit(val=None, strict=False):
    while True:
        if val is None:
            val = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        has_digit = any(c.isdigit() for c in val)
        has_alpha = any(c.isalpha() for c in val)
        if has_digit and (not strict or has_alpha):
            return val
        val = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

patterns = {
    "1": ("X_XXX", lambda: f"{random.choice(string.ascii_uppercase)}_{''.join(random.choices(string.ascii_uppercase, k=3))}"),
    "2": ("XX_XX", lambda: f"{''.join(random.choices(string.ascii_uppercase, k=2))}_{''.join(random.choices(string.ascii_uppercase, k=2))}"),
    "3": ("XXX_X", lambda: f"{''.join(random.choices(string.ascii_uppercase, k=3))}_{random.choice(string.ascii_uppercase)}"),
    "4": ("1_X2X", lambda: gen_pat_digit(f"{random.choice(string.ascii_uppercase + string.digits)}_{random.choice(string.ascii_uppercase)}{random.choice(string.digits)}{random.choice(string.ascii_uppercase)}")),
    "5": ("1X_2X", lambda: gen_pat_digit(f"{random.choice(string.ascii_uppercase + string.digits)}{random.choice(string.ascii_uppercase)}_{random.choice(string.digits)}{random.choice(string.ascii_uppercase)}")),
    "6": ("1X2_X", lambda: gen_pat_digit(f"{random.choice(string.ascii_uppercase + string.digits)}{random.choice(string.ascii_uppercase)}{random.choice(string.digits)}_{random.choice(string.ascii_uppercase)}")),
    "7": ("X1X2X", lambda: gen_pat_digit(strict=True))
}

for key, (desc, gen_fn) in patterns.items():
    example1 = gen_fn()
    example2 = gen_fn()
    print(f"{key}. {desc}  (e.g. {example1}, {example2})")

print("8. Custom pattern (e.g., LLDLD → MQ9F5, VZ3P0)")
print("9. Load from .txt file")

choice = input("\nEnter your choice: ").strip()

def rand_char(c):
    if c == "L":
        return random.choice(string.ascii_uppercase)
    elif c == "D":
        return random.choice(string.digits)
    return c

def gen_from_fmt(fmt):
    return ''.join(rand_char(c) for c in fmt)

def chk_user(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?username={username}&birthday=2001-09-11"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.json().get("code")
    except Exception as e:
        print(f"Error checking {username}: {e}")
    return None

usernames = []

if choice == "9":
    path = input("Enter path to .txt file: ").strip()
    if os.path.exists(path):
        with open(path, 'r') as file:
            usernames = [line.strip() for line in file if line.strip()]
    else:
        print("Invalid file path.")
        exit()

elif choice == "8":
    pattern = input("Enter your custom pattern using L (letter) and D (digit): ").strip().upper()
    num = int(input("How many usernames to check? "))
    usernames = [gen_from_fmt(pattern) for _ in range(num)]

elif choice in patterns:
    _, gen_fn = patterns[choice]
    num = int(input("How many usernames to check? "))
    usernames = [gen_fn() for _ in range(num)]

else:
    print("Invalid option.")
    exit()

for fname in ["valid.txt", "taken.txt", "censored.txt"]:
    open(fname, "w").close()

print("\nChecking usernames...\n")

for name in usernames:
    code = chk_user(name)
    if code == 0:
        print(Fore.GREEN + f"[VALID] Username valid: {name}")
        with open("valid.txt", "a") as f:
            f.write(name + "\n")
    elif code == 1:
        print(Fore.WHITE + f"[TAKEN] Username taken: {name}")
        with open("taken.txt", "a") as f:
            f.write(name + "\n")
    elif code == 2:
        print(Fore.RED + f"[CENSORED] Username censored: {name}")
        with open("censored.txt", "a") as f:
            f.write(name + "\n")
    else:
        print(f"Unknown error for: {name}")

print("\nDone! Results saved to:")
print("  - valid.txt")
print("  - taken.txt")
print("  - censored.txt")

#!/usr/bin/env python3
"""
Username Sniper - One-Command Setup Script
Run: python startup.py
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

def print_header():
    print(f"{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║   Username Sniper - One-Command Setup                 ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")

def check_python():
    print(f"{Colors.YELLOW}[1/5]{Colors.END} Checking Python...")
    if sys.version_info < (3, 8):
        print(f"{Colors.RED}✗ Python 3.8+ required (you have {sys.version}){Colors.END}")
        return False
    print(f"{Colors.GREEN}✓ Python {sys.version.split()[0]} OK{Colors.END}")
    return True

def install_requirements():
    print(f"{Colors.YELLOW}[2/5]{Colors.END} Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
        print(f"{Colors.GREEN}✓ Dependencies installed{Colors.END}")
        return True
    except subprocess.CalledProcessError:
        print(f"{Colors.RED}✗ Failed to install requirements{Colors.END}")
        return False

def setup_env():
    print(f"{Colors.YELLOW}[3/5]{Colors.END} Setting up .env file...")
    env_path = Path(".env")
    env_example = Path(".env.example")
    
    if not env_example.exists():
        print(f"{Colors.RED}✗ .env.example not found{Colors.END}")
        return False
    
    if env_path.exists():
        print(f"{Colors.GREEN}✓ .env already exists{Colors.END}")
        return True
    
    try:
        shutil.copy(".env.example", ".env")
        print(f"{Colors.GREEN}✓ .env created from template{Colors.END}")
        return True
    except Exception as e:
        print(f"{Colors.RED}✗ Failed to create .env: {e}{Colors.END}")
        return False

def verify_files():
    print(f"{Colors.YELLOW}[4/5]{Colors.END} Verifying files...")
    required_files = ["main.py", "discord_bot.py", ".env", "requirements.txt"]
    all_ok = True
    
    for file in required_files:
        if Path(file).exists():
            print(f"{Colors.GREEN}✓ {file}{Colors.END}")
        else:
            print(f"{Colors.RED}✗ {file} missing{Colors.END}")
            all_ok = False
    
    return all_ok

def make_executable():
    print(f"{Colors.YELLOW}[5/5]{Colors.END} Setting up scripts...")
    scripts = ["setup.sh", "setup.bat"]
    
    for script in scripts:
        script_path = Path(script)
        if script_path.exists() and script == "setup.sh":
            try:
                os.chmod(script, 0o755)
                print(f"{Colors.GREEN}✓ {script} executable{Colors.END}")
            except:
                pass

def main():
    print_header()
    print()
    
    steps = [
        ("Python check", check_python),
        ("Install requirements", install_requirements),
        ("Setup .env", setup_env),
        ("Verify files", verify_files),
        ("Make scripts executable", make_executable),
    ]
    
    for name, func in steps:
        if not func():
            print(f"\n{Colors.RED}✗ Setup failed at: {name}{Colors.END}")
            sys.exit(1)
    
    print()
    print(f"{Colors.BLUE}════════════════════════════════════════════════════════{Colors.END}")
    print(f"{Colors.GREEN}✓ Setup Complete!{Colors.END}")
    print(f"{Colors.BLUE}════════════════════════════════════════════════════════{Colors.END}")
    print()
    print(f"{Colors.YELLOW}📝 NEXT STEPS:{Colors.END}")
    print()
    print("1. Edit .env with your Discord bot token:")
    print(f"   {Colors.BLUE}nano .env{Colors.END} (Linux/Mac) or {Colors.BLUE}notepad .env{Colors.END} (Windows)")
    print()
    print("2. Run CLI version:")
    print(f"   {Colors.BLUE}python main.py{Colors.END}")
    print()
    print("3. Or run Discord bot:")
    print(f"   {Colors.BLUE}python discord_bot.py{Colors.END}")
    print()
    print(f"{Colors.YELLOW}📚 Documentation:{Colors.END}")
    print("   - QUICK_START.md")
    print("   - DISCORD_BOT_SETUP.md")
    print("   - COMPARISON.md")
    print()

if __name__ == "__main__":
    main()

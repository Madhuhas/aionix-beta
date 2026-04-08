import time
import sys
import os
import random

# ANSI colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_bar(task, length=22, speed=0.03):
    sys.stdout.write(f"{CYAN}{task}{RESET} [")
    sys.stdout.flush()
    for _ in range(length):
        sys.stdout.write(f"{GREEN}#{RESET}")
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write(f"] {GREEN}OK{RESET}\n")
    sys.stdout.flush()

def boot_logo():
    logo = f"""
{CYAN}{BOLD}
    █████╗ ██╗ ██████╗  ███╗   ██╗██╗██╗  ██╗
   ██╔══██╗██║██╔═══██╗ ████╗  ██║██║╚██╗██╔╝
   ███████║██║██║   ██║ ██╔██╗ ██║██║ ╚███╔╝ 
   ██╔══██║██║██║   ██║ ██║╚██╗██║██║ ██╔██╗ 
   ██║  ██║██║╚██████╔╝ ██║ ╚████║██║██╔╝ ██╗
   ╚═╝  ╚═╝╚═╝ ╚═════╝  ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝

              A  I  O  N  I  X   O  S
{RESET}
"""
    print(logo)
    time.sleep(0.5)

def random_boot_message():
    messages = [
        "Linking cognitive subsystems...",
        "Synchronizing persona matrix...",
        "Priming intent engine...",
        "Stabilizing command pipeline...",
        "Verifying system integrity...",
        "Aligning AIONIX core protocols...",
        "Calibrating adaptive reasoning layer...",
        "Registering shell environment...",
        "Preparing interactive session...",
        "Bringing AIONIX online..."
    ]
    slow_print(f"{YELLOW}{random.choice(messages)}{RESET}", 0.02)
    time.sleep(0.3)

def boot_sequence():
    os.system("cls" if os.name == "nt" else "clear")

    boot_logo()
    slow_print(f"{CYAN}Initializing AIONIX OS...{RESET}\n", 0.04)

    loading_bar("Loading kernel        ")
    loading_bar("Mounting filesystem   ")
    loading_bar("Starting services     ")
    loading_bar("Loading persona core  ")
    loading_bar("Checking system       ")

    for _ in range(3):
        random_boot_message()

    slow_print(f"\n{GREEN}{BOLD}AIONIX OS Ready.{RESET}\n", 0.04)
    time.sleep(0.4)

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import subprocess
import datetime
import json
import requests

from ai_os.shell.boot import boot_sequence
from ai_os.persona.persona_core import PersonaCore
from ai_os.file_manager.file_engine import FileEngine
from ai_os.app_launcher.launcher import AppLauncher
from ai_os.memory.memory_engine import MemoryEngine
from ai_os.platform.platform_core import load_platform
from ai_os.voice.voice_engine import VoiceEngine
from ai_os.system.system_monitor import SystemMonitor
from ai_os.package_manager.package_manager import PackageManager

BANNER = r"""
=============================
        AIONIX OS Beta
        © Kotini
=============================
"""

LOG_FILE = "ai_os_shell.log"
MODEL_NAME = "qwen2.5:0.5b"
OLLAMA_URL = "http://localhost:11434/api/generate"

# Platform + engines
platform = load_platform()
persona = PersonaCore()
file_engine = FileEngine()
memory = MemoryEngine()
launcher = AppLauncher(platform)
voice = VoiceEngine()
monitor = SystemMonitor()
pkg = PackageManager(platform)

# Load preferred persona
persona.set_persona(memory.get_preferred_persona())


def log_event(user_input: str, command: str, exit_code: int):
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")
    line = f"{timestamp} | input='{user_input}' | command='{command}' | exit={exit_code}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass


def call_ollama(prompt: str) -> str:
    print(f">>> DEBUG: Calling Ollama model: {MODEL_NAME}")
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            timeout=120
        )
        data = response.json()
        raw = data.get("response", "")
        print(">>> DEBUG: Ollama raw response:", raw)
        return raw
    except Exception as e:
        print(">>> DEBUG: Ollama ERROR:", str(e))
        return json.dumps({
            "command": f"echo Ollama error: {str(e)}",
            "reason": "ollama_error"
        })


def clean_json(raw: str) -> str:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()
    return cleaned


def fix_windows_command(cmd: str) -> str:
    lower = cmd.lower()
    if lower.startswith("ping ") and "-c" in lower:
        return cmd.replace("-c", "-n")
    if lower.startswith("ls"):
        return "dir"
    if lower.startswith("cat "):
        return cmd.replace("cat", "type", 1)
    if lower == "clear":
        return "cls"
    if lower == "pwd":
        return "cd"
    return cmd


def validate_command(cmd: str) -> str:
    invalid = [
        "reply", "say", "speak", "respond", "talk", "message",
        "sayhello", "hello", "hi", "greet", "greeting"
    ]
    if cmd.lower() in invalid:
        return 'echo I am in command mode, not chat mode.'
    if not cmd.strip():
        return 'echo I am not sure what to do.'
    return cmd


def nl_to_command(user_input: str):
    text = user_input.strip().lower()

    # conversational bypass
    chatlike = ["hi", "hello", "hey", "how are you", "yo", "sup"]
    if text in chatlike:
        return 'echo Hello! I am AIONIX OS.', "friendly greeting"

    # user-defined shortcuts
    shortcut = memory.get_shortcut(text)
    if shortcut:
        return shortcut, f"shortcut: {text}"

    # system monitor commands
    if "system status" in text or "system info" in text:
        return "__sys_status__", "show system status"

    if "cpu usage" in text:
        return "__sys_cpu__", "show cpu usage"

    if "ram usage" in text or "memory usage" in text:
        return "__sys_ram__", "show ram usage"

    if "disk usage" in text:
        return "__sys_disk__", "show disk usage"

    if "network usage" in text:
        return "__sys_net__", "show network usage"

    if "list processes" in text:
        return "__sys_procs__", "list processes"

    if text.startswith("kill process "):
        pid = text.replace("kill process ", "").strip()
        return f"__sys_kill__:{pid}", f"kill process {pid}"

    # package manager commands
    if text.startswith("install "):
        pkg_name = text.replace("install ", "").strip()
        return f"__pkg_install__:{pkg_name}", f"install {pkg_name}"

    if text.startswith("uninstall "):
        pkg_name = text.replace("uninstall ", "").strip()
        return f"__pkg_uninstall__:{pkg_name}", f"uninstall {pkg_name}"

    if text.startswith("search package "):
        query = text.replace("search package ", "").strip()
        return f"__pkg_search__:{query}", f"search package {query}"

    if text.startswith("update package "):
        pkg_name = text.replace("update package ", "").strip()
        return f"__pkg_update__:{pkg_name}", f"update package {pkg_name}"

    if text == "update all":
        return "__pkg_update_all__", "update all packages"

    if text == "list installed apps":
        return "__pkg_list__", "list installed apps"

    # file manager intents
    if "list files" in text or "show files" in text:
        return "__file_list__", "list files"

    if text.startswith("find ") and "." in text:
        ext = text.split()[-1].replace(".", "")
        return f"__file_find__:{ext}", f"find .{ext}"

    if text.startswith("copy ") and " to " in text:
        parts = text[5:].split(" to ")
        src = parts[0].strip()
        dest = parts[1].strip()
        return f"__file_copy__:{src}:{dest}", f"copy {src} to {dest}"

    if text.startswith("delete "):
        pattern = text[7:].strip()
        return f"__file_delete__:{pattern}", f"delete {pattern}"

    if text.startswith("rename ") and " to " in text:
        parts = text[7:].split(" to ")
        old_ext = parts[0].replace(".", "").strip()
        new_ext = parts[1].replace(".", "").strip()
        return f"__file_rename__:{old_ext}:{new_ext}", f"rename .{old_ext} to .{new_ext}"

    # app launcher intents
    if text.startswith("open "):
        target = user_input[5:].strip()
        return f"__launch__:{target}", f"launch {target}"

    # save shortcut
    if text.startswith("remember this as "):
        keyword = text.replace("remember this as ", "").strip()
        return f"__save_shortcut__:{keyword}", f"save shortcut {keyword}"

    # fall back to LLM
    prompt = persona.rewrite_prompt(user_input)
    raw = call_ollama(prompt)
    cleaned = clean_json(raw)

    try:
        parsed = json.loads(cleaned)
        cmd = parsed.get("command", "").strip()
        reason = parsed.get("reason", "").strip()
        cmd = fix_windows_command(cmd)
        cmd = validate_command(cmd)
        print(">>> DEBUG: Parsed command:", cmd)
        return cmd, reason or "AI-interpreted command"
    except Exception:
        return f'echo Could not understand: "{user_input}"', "fallback"


def run_command(cmd: str):
    result = subprocess.run(
        cmd,
        shell=True,
        text=True,
        capture_output=True
    )
    return result.stdout, result.stderr, result.returncode


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    boot_sequence()

    print(BANNER)
    print("Hello, I am your OS. Type 'exit' to quit.\n")
    print("Personas: friendly, minimal, playful, dev")
    print("Use: set persona <name>\n")
    print("Shortcuts: 'remember this as <name>'")
    print("Voice: type 'voice' to speak a command.")
    print("System Monitor: 'system status', 'cpu usage', 'list processes'")
    print("Packages: 'install vscode', 'update all', 'list installed apps'\n")

    last_command = None

    while True:
        try:
            user_input = input("ai-os >> ")
        except (EOFError, KeyboardInterrupt):
            print("\nShutting down AIONIX OS. Goodbye.")
            break

        if user_input.strip().lower() in ("exit", "quit"):
            print("Shutting down AIONIX OS. Goodbye.")
            break

        # persona switching
        if user_input.startswith("set persona "):
            name = user_input.replace("set persona ", "").strip()
            if persona.set_persona(name):
                memory.remember_persona(name)
                print(f"Persona switched to: {name}")
            else:
                print("Unknown persona. Options: friendly, minimal, playful, dev")
            continue

        # voice mode
        if user_input.strip().lower() == "voice":
            spoken = voice.listen_once()
            if not spoken:
                continue
            user_input = spoken

        if not user_input.strip():
            continue

        command, reason = nl_to_command(user_input)

        # system monitor commands
        if command == "__sys_status__":
            print("CPU:", monitor.get_cpu(), "%")
            print("RAM:", monitor.get_ram())
            print("Disk:", monitor.get_disk())
            print("Network:", monitor.get_network())
            print("Uptime:", monitor.get_uptime())
            continue

        if command == "__sys_cpu__":
            print("CPU Usage:", monitor.get_cpu(), "%")
            continue

        if command == "__sys_ram__":
            print("RAM:", monitor.get_ram())
            continue

        if command == "__sys_disk__":
            print("Disk:", monitor.get_disk())
            continue

        if command == "__sys_net__":
            print("Network:", monitor.get_network())
            continue

        if command == "__sys_procs__":
            for p in monitor.get_processes():
                print(p)
            continue

        if command.startswith("__sys_kill__"):
            pid = int(command.split(":", 1)[1])
            print(monitor.kill_process(pid))
            continue

        # package manager commands
        if command.startswith("__pkg_install__"):
            pkg_name = command.split(":", 1)[1]
            print(pkg.install(pkg_name))
            continue

        if command.startswith("__pkg_uninstall__"):
            pkg_name = command.split(":", 1)[1]
            print(pkg.uninstall(pkg_name))
            continue

        if command.startswith("__pkg_search__"):
            query = command.split(":", 1)[1]
            print(pkg.search(query))
            continue

        if command.startswith("__pkg_update__"):
            pkg_name = command.split(":", 1)[1]
            print(pkg.update(pkg_name))
            continue

        if command == "__pkg_update_all__":
            print(pkg.update())
            continue

        if command == "__pkg_list__":
            print(pkg.list_installed())
            continue

        # save shortcut
        if command.startswith("__save_shortcut__"):
            keyword = command.split(":", 1)[1]
            if last_command:
                memory.add_shortcut(keyword, last_command)
                print(f"Shortcut '{keyword}' saved.")
            else:
                print("No previous command to save as shortcut.")
            continue

        # file engine commands
        if command.startswith("__file_list__"):
            print("\n".join(file_engine.list_files()))
            memory.add_command(user_input)
            last_command = command
            continue

        if command.startswith("__file_find__"):
            ext = command.split(":", 1)[1]
            files = file_engine.find_by_extension(ext)
            print("\n".join(files) if files else f"No .{ext} files found.")
            memory.add_command(user_input)
            last_command = command
            continue

        if command.startswith("__file_copy__"):
            _, src, dest = command.split(":", 2)
            print("\n".join(file_engine.copy_files(src, dest)))
            memory.add_command(user_input)
            last_command = command
            continue

        if command.startswith("__file_delete__"):
            pattern = command.split(":", 1)[1]
            print("\n".join(file_engine.delete_files(pattern)))
            memory.add_command(user_input)
            last_command = command
            continue

        if command.startswith("__file_rename__"):
            _, old_ext, new_ext = command.split(":", 2)
            print("\n".join(file_engine.rename_extension(old_ext, new_ext)))
            memory.add_command(user_input)
            last_command = command
            continue

        # app launcher commands
        if command.startswith("__launch__"):
            target = command.split(":", 1)[1]
            result = launcher.launch(target)
            print(result)
            voice.speak(result)
            memory.add_command(user_input)
            last_command = command
            continue

        # normal command flow
        rendered = persona.rewrite_response(command, reason)
        print(rendered)
        voice.speak(rendered)

        stdout, stderr, code = run_command(command)
        if stdout:
            print(stdout, end="")
        if stderr:
            print(stderr, end="")
        print(f"[exit code: {code}]")

        memory.add_command(user_input)
        last_command = command


if __name__ == "__main__":
    main()

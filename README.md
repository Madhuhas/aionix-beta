# AIONIX (Beta)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/) [![GitHub Repo](https://img.shields.io/badge/github-Madhuhas%2Faionix--beta-blue)](https://github.com/Madhuhas/aionix-beta)

AIONIX is an experimental AI-powered shell prototype that turns natural language into local OS commands. It combines a conversational prompt layer with modular engines for voice I/O, memory, file management, package control, system monitoring, and app launching.

> AIONIX is built as a local, Windows-first AI shell with Linux compatibility and a modular engine architecture.

## 🚀 Key Features

- **Natural language command generation** through a local Ollama model (`qwen2.5:0.5b`) via `http://localhost:11434/api/generate`
- **Persona-driven prompt rewriting** with ready-made personas: `friendly`, `minimal`, `playful`, `dev`
- **Voice assistant support** using `speech_recognition` and `pyttsx3`
- **Persistent memory** for preferred persona, shortcuts, favorite paths, and history
- **File management utilities**: list, search by extension, copy, delete, rename extension
- **Package management** via Winget on Windows: install, uninstall, search, update, list
- **System monitoring** through `psutil`: CPU, RAM, disk, network, processes, uptime
- **Cross-platform abstraction** with a `platform/` module for Windows and Linux behavior
- **Shell experience** with animated boot sequence, command validation, and AI fallback handling

## 📁 Architecture Overview

AIONIX is composed of distinct engines and a shell orchestrator:

- `shell/main.py` — entry point, user input loop, command routing, Ollama integration
- `shell/boot.py` — boot animation and startup visuals
- `app_launcher/launcher.py` — launch apps and open favorite folders
- `file_manager/file_engine.py` — file utilities for list, find, copy, delete, rename
- `memory/memory_engine.py` — persistent JSON memory store for shortcuts and preferences
- `persona/persona_core.py` — loads and switches persona modules dynamically
- `package_manager/package_manager.py` — winget-based package operations on Windows
- `platform/platform_core.py` — environment detection and platform adapter selection
- `system/system_monitor.py` — resource monitoring built on `psutil`
- `voice/voice_engine.py` — speech recognition and text-to-speech bridge

## 🧠 How It Works

1. User enters a command or natural language prompt in `shell/main.py`
2. The shell checks for built-in intents and shortcuts
3. If needed, the input is rewritten by a persona module and sent to Ollama
4. Ollama returns JSON-style instructions that are cleaned and validated
5. The command executes via subprocess/platform adapters
6. Results are displayed, and relevant memory/history is persisted

## ▶️ Quick Start

### Requirements

- Python 3.11+ (recommended)
- `pip install -r requirements` or install:
  - `requests`
  - `psutil`
  - `speech_recognition`
  - `pyttsx3`
- Local Ollama server with `qwen2.5:0.5b`
- Windows: `winget` for package management features

### Run the shell

```bash
python shell/main.py
```

### Example commands

- `open chrome`
- `install vscode`
- `search package python`
- `list files`
- `find .py`
- `system status`
- `cpu usage`
- `list processes`
- `set persona playful`
- `remember this as quickdocs`
- `voice`

## 🧪 Live Demo

Use the shell in a live session with commands like this:

```bash
python shell/main.py
```

```text
ai-os >> open chrome
ai-os >> install vscode
ai-os >> system status
ai-os >> remember this as worktools
ai-os >> open desktop
```

This session demonstrates AIONIX interpreting natural language, launching apps, querying system metrics, and saving custom shortcuts.

## 🛠️ Supported Command Patterns

AIONIX recognizes both direct intent commands and AI-generated fallback commands.

Native command examples:

- `install <package>`
- `uninstall <package>`
- `search package <query>`
- `update package <package>`
- `update all`
- `list installed apps`
- `list files`
- `find <extension>`
- `copy <src> to <dest>`
- `delete <pattern>`
- `rename <old_ext> to <new_ext>`
- `open <app or folder>`
- `system status`
- `cpu usage`
- `ram usage`
- `disk usage`
- `network usage`
- `list processes`
- `kill process <pid>`

## 🛡️ Safety & Behavior

- Built-in validation blocks conversational commands like `say`, `speak`, and `talk` when AIONIX is in command mode
- Commands are sanitized and Windows translations are applied automatically (e.g. `ls` → `dir`, `cat` → `type`, `pwd` → `cd`)
- AI fallback is used only when no direct intent is identified

## 🌍 Platform Support

- `platform/windows.py` — Windows file opening, app launching, screen clearing, Winget integration
- `platform/linux.py` — Linux path opening, app commands, and defaults via `xdg-open`

## ✨ Project Goals

AIONIX is a beta prototype with these goals:

- create a voice-enabled AI shell experience
- provide a modular architecture suitable for expansion
- support custom personas and memory-driven workflows
- build a bridge between natural language and local OS operations

## 📌 Notes

- The project is currently Windows-first, with Linux compatibility through platform abstraction
- Ollama must be running locally for AI-powered prompt interpretation
- Voice support requires microphone access and TTS dependencies

## 🔧 Contribution

This repo is ideal for contributors who want to improve:

- language intent parsing
- shell safety and sandboxing
- Linux compatibility and desktop integration
- voice UX and persona behaviors
- model prompt engineering and offline AI command generation

Read the full contribution guide in [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

AIONIX is released under the [MIT License](LICENSE).

---

© Madhuhas / Kotini


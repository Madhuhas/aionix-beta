import os
import subprocess

class WindowsPlatform:

    def clear_screen(self):
        os.system("cls")

    def open_path(self, path):
        os.startfile(path)

    def run_app(self, command):
        # Used both for launching apps and running shell commands (winget, etc.)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.stdout else f"Executed: {command}"

    def get_default_paths(self):
        user = os.getenv("USERNAME")
        base = f"C:\\Users\\{user}"

        return {
            "downloads": f"{base}\\Downloads",
            "documents": f"{base}\\Documents",
            "pictures": f"{base}\\Pictures",
            "desktop": f"{base}\\Desktop"
        }

    def get_default_apps(self):
        user = os.getenv("USERNAME")

        return {
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "vscode": fr"C:\Users\{user}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            "code": fr"C:\Users\{user}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "task manager": "taskmgr.exe",
            "control panel": "control.exe",
            "settings": "start ms-settings:"
        }

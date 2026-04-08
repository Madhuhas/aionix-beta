import os
import subprocess

class LinuxPlatform:

    def clear_screen(self):
        os.system("clear")

    def open_path(self, path):
        subprocess.Popen(["xdg-open", path])

    def run_app(self, command):
        subprocess.Popen(command.split())

    def get_default_paths(self):
        home = os.path.expanduser("~")
        return {
            "downloads": f"{home}/Downloads",
            "documents": f"{home}/Documents",
            "pictures": f"{home}/Pictures"
        }

    def get_default_apps(self):
        return {
            "chrome": "google-chrome",
            "vscode": "code",
            "notepad": "gedit",
            "calculator": "gnome-calculator",
            "task manager": "gnome-system-monitor",
            "control panel": "gnome-control-center",
            "settings": "gnome-control-center"
        }

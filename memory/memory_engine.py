import json
import os

class MemoryEngine:

    def __init__(self):
        self.memory_file = os.path.join(os.path.dirname(__file__), "memory.json")
        self.data = {
            "preferred_persona": "friendly",
            "favorite_paths": {},
            "command_history": [],
            "shortcuts": {}
        }
        self.load()

    def load(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except:
                pass

    def save(self):
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        except:
            pass

    # ---- Memory Features ----

    def remember_persona(self, persona):
        self.data["preferred_persona"] = persona
        self.save()

    def get_preferred_persona(self):
        return self.data.get("preferred_persona", "friendly")

    def add_command(self, cmd):
        self.data["command_history"].append(cmd)
        self.data["command_history"] = self.data["command_history"][-50:]
        self.save()

    def remember_path(self, name, path):
        self.data["favorite_paths"][name] = path
        self.save()

    def get_path(self, name):
        return self.data["favorite_paths"].get(name)

    def add_shortcut(self, keyword, action):
        self.data["shortcuts"][keyword] = action
        self.save()

    def get_shortcut(self, keyword):
        return self.data["shortcuts"].get(keyword)

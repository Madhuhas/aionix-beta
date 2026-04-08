import json
import os
import importlib

class PersonaCore:
    def __init__(self):
        self.persona_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.persona_dir, "config.json")
        self.personas = {
            "friendly": "friendly",
            "minimal": "minimal",
            "playful": "playful",
            "dev": "dev_mode"
        }
        self.active_persona = "friendly"
        self.module = None
        self.load_config()
        self.load_persona_module()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.active_persona = data.get("active_persona", "friendly")

    def save_config(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump({"active_persona": self.active_persona}, f, indent=4)

    def load_persona_module(self):
        module_name = self.personas.get(self.active_persona, "friendly")
        module_path = f"ai_os.persona.{module_name}"
        self.module = importlib.import_module(module_path)

    def set_persona(self, name: str) -> bool:
        if name not in self.personas:
            return False
        self.active_persona = name
        self.save_config()
        self.load_persona_module()
        return True

    def rewrite_prompt(self, user_input: str) -> str:
        return self.module.rewrite_prompt(user_input)

    def rewrite_response(self, command: str, reason: str) -> str:
        return self.module.rewrite_response(command, reason)

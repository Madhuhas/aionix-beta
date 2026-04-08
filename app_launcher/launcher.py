class AppLauncher:

    def __init__(self, platform):
        self.platform = platform
        self.apps = platform.get_default_apps()
        self.paths = platform.get_default_paths()

    def launch(self, target):
        target = target.lower().strip()

        # folder launch
        if target in self.paths:
            self.platform.open_path(self.paths[target])
            return f"Opened {target}."

        # app launch
        if target in self.apps:
            self.platform.run_app(self.apps[target])
            return f"Launched {target}."

        return f"Unknown app or folder: {target}"

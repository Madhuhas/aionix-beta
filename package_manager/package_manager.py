import subprocess

class PackageManager:

    def __init__(self, platform):
        self.platform = platform

    def install(self, package):
        cmd = f"winget install --id {package} -e --silent"
        return self.platform.run_app(cmd)

    def uninstall(self, package):
        cmd = f"winget uninstall --id {package} -e"
        return self.platform.run_app(cmd)

    def search(self, query):
        cmd = f"winget search {query}"
        return self.platform.run_app(cmd)

    def update(self, package=None):
        if package:
            cmd = f"winget upgrade --id {package} -e"
        else:
            cmd = "winget upgrade --all"
        return self.platform.run_app(cmd)

    def list_installed(self):
        cmd = "winget list"
        return self.platform.run_app(cmd)

import platform
from ai_os.platform.windows import WindowsPlatform
from ai_os.platform.linux import LinuxPlatform

def load_platform():
    system = platform.system().lower()

    if "windows" in system:
        return WindowsPlatform()

    if "linux" in system:
        return LinuxPlatform()

    # fallback
    return WindowsPlatform()

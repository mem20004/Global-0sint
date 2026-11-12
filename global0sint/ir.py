import sys
import subprocess
import platform

def main():
    packages = ["requests", "beautifulsoup4", "lxml", "fake-useragent"]
    system = platform.system().lower()

    if system == "windows":
        cmd = [sys.executable, "-m", "pip", "install"] + packages
    elif system == "linux":
        cmd = ["pip", "install"] + packages
    elif system == "darwin":
        cmd = ["pip3", "install"] + packages
    else:
        print("Unknown OS. Install manually:")
        print("pip install " + " ".join(packages))
        return

    print(f"Running: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        print("All packages installed.")
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")

if __name__ == "__main__":
    main()


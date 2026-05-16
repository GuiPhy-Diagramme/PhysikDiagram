import os
import sys
import subprocess

REQUIREMENTS_FILE = "requirements.txt"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(BASE_DIR, "libs")
REQUIREMENTS_PATH = os.path.join(BASE_DIR, REQUIREMENTS_FILE)
os.makedirs(LIBS_DIR, exist_ok=True)

sys.path.insert(0, LIBS_DIR)
needs_install = False
try:
    with open(REQUIREMENTS_PATH, "r") as f:
        for line in f:
            package = line.strip()
            if not package or package.startswith("#"):
                continue
            module_name = package.split("==")[0]
            try:
                __import__(module_name)
            except ImportError:
                needs_install = True
                break
except FileNotFoundError:
    print(f"Missing {REQUIREMENTS_FILE}")
    sys.exit(1)
    
if needs_install:
    print("Installing dependencies...\n")
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-t",
        LIBS_DIR,
        "-r",
        REQUIREMENTS_PATH
    ])
    print("\nDependencies installed.\n")
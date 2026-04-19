import json
import os
import shutil

PACKAGES_DIR  = os.path.join(os.path.expanduser("~"), ".untold", "packages")
CACHE_DIR     = os.path.join(os.path.expanduser("~"), ".untold", "cache")
REGISTRY_URL  = "https://raw.githubusercontent.com/untold-lang/registry/main"

# Built-in package registry (local for now — Phase 6 will be remote)
BUILTIN_REGISTRY = {
    "colors": {
        "version":     "1.0.0",
        "description": "Terminal color output for Untold Lang",
        "author":      "untold-core",
        "builtin":     True
    },
    "dotenv": {
        "version":     "1.0.0",
        "description": "Load .env files into untold.shell.env()",
        "author":      "untold-core",
        "builtin":     True
    },
    "uuid": {
        "version":     "1.0.0",
        "description": "Generate UUIDs",
        "author":      "untold-core",
        "builtin":     True
    },
    "crypto": {
        "version":     "1.0.0",
        "description": "Extended crypto utilities",
        "author":      "untold-core",
        "builtin":     True
    },
    "argparse": {
        "version":     "1.0.0",
        "description": "Parse CLI arguments in .ut scripts",
        "author":      "untold-core",
        "builtin":     True
    },
}

def ensure_dirs():
    os.makedirs(PACKAGES_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR,    exist_ok=True)

def pkg_install(name, version=None, config=None):
    ensure_dirs()

    print(f"[utpkg] Installing '{name}'...")

    # Check built-in registry
    if name in BUILTIN_REGISTRY:
        info    = BUILTIN_REGISTRY[name]
        pkg_dir = os.path.join(PACKAGES_DIR, name)
        os.makedirs(pkg_dir, exist_ok=True)

        # Write the built-in package implementation
        _write_builtin_package(name, pkg_dir)

        ver = version or info["version"]
        print(f"[utpkg] Installed {name}@{ver} — {info['description']}")

        # Update untold.json
        if config is not None:
            config["dependencies"][name] = ver
        return True

    print(f"[utpkg] Package '{name}' not found in registry.")
    print(f"[utpkg] Available packages: {', '.join(BUILTIN_REGISTRY.keys())}")
    return False

def pkg_remove(name, config=None):
    pkg_dir = os.path.join(PACKAGES_DIR, name)
    if os.path.exists(pkg_dir):
        shutil.rmtree(pkg_dir)
        print(f"[utpkg] Removed '{name}'")
        if config and name in config.get("dependencies", {}):
            del config["dependencies"][name]
        return True
    print(f"[utpkg] Package '{name}' is not installed")
    return False

def pkg_list():
    ensure_dirs()
    installed = []
    if os.path.exists(PACKAGES_DIR):
        for name in os.listdir(PACKAGES_DIR):
            pkg_json = os.path.join(PACKAGES_DIR, name, "package.json")
            if os.path.exists(pkg_json):
                with open(pkg_json) as f:
                    info = json.load(f)
                installed.append((name, info.get("version", "?")))
    return installed

def pkg_search(query):
    results = []
    for name, info in BUILTIN_REGISTRY.items():
        if query.lower() in name.lower() or query.lower() in info["description"].lower():
            results.append((name, info["version"], info["description"]))
    return results

def pkg_install_all(config):
    """Install all dependencies from untold.json"""
    deps = config.get("dependencies", {})
    if not deps:
        print("[utpkg] No dependencies to install")
        return
    for name, version in deps.items():
        pkg_install(name, version, config)

def _write_builtin_package(name, pkg_dir):
    """Write the actual package code to disk."""
    implementations = {
        "colors": '''
import sys

class Colors:
    RED     = "\\033[91m"
    GREEN   = "\\033[92m"
    YELLOW  = "\\033[93m"
    BLUE    = "\\033[94m"
    PURPLE  = "\\033[95m"
    CYAN    = "\\033[96m"
    WHITE   = "\\033[97m"
    BOLD    = "\\033[1m"
    RESET   = "\\033[0m"

    @staticmethod
    def red(text):     return f"{Colors.RED}{text}{Colors.RESET}"
    @staticmethod
    def green(text):   return f"{Colors.GREEN}{text}{Colors.RESET}"
    @staticmethod
    def yellow(text):  return f"{Colors.YELLOW}{text}{Colors.RESET}"
    @staticmethod
    def blue(text):    return f"{Colors.BLUE}{text}{Colors.RESET}"
    @staticmethod
    def purple(text):  return f"{Colors.PURPLE}{text}{Colors.RESET}"
    @staticmethod
    def cyan(text):    return f"{Colors.CYAN}{text}{Colors.RESET}"
    @staticmethod
    def bold(text):    return f"{Colors.BOLD}{text}{Colors.RESET}"
    @staticmethod
    def say_red(text):    print(f"{Colors.RED}{text}{Colors.RESET}")
    @staticmethod
    def say_green(text):  print(f"{Colors.GREEN}{text}{Colors.RESET}")
    @staticmethod
    def say_yellow(text): print(f"{Colors.YELLOW}{text}{Colors.RESET}")
    @staticmethod
    def say_blue(text):   print(f"{Colors.BLUE}{text}{Colors.RESET}")
''',
        "dotenv": '''
import os

class DotEnv:
    @staticmethod
    def load(path=".env"):
        if not os.path.exists(path):
            return False
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip(\'"\\'\\' \')
        return True

    @staticmethod
    def get(key, default=None):
        return os.environ.get(key, default)
''',
        "uuid": '''
import uuid as _uuid

class UUID:
    @staticmethod
    def v4():
        return str(_uuid.uuid4())

    @staticmethod
    def v1():
        return str(_uuid.uuid1())

    @staticmethod
    def short():
        return str(_uuid.uuid4())[:8]
''',
        "crypto": '''
import hashlib, hmac, base64, os, secrets

class Crypto:
    @staticmethod
    def hash(text, algo="sha256"):
        h = hashlib.new(algo)
        h.update(text.encode())
        return h.hexdigest()

    @staticmethod
    def hmac_sign(key, msg):
        return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def random_token(n=32):
        return secrets.token_hex(int(n))

    @staticmethod
    def random_int(low, high):
        return secrets.randbelow(int(high) - int(low)) + int(low)

    @staticmethod
    def b64_encode(text):
        return base64.b64encode(text.encode()).decode()

    @staticmethod
    def b64_decode(text):
        return base64.b64decode(text.encode()).decode(errors="replace")
''',
        "argparse": '''
import sys

class ArgParser:
    @staticmethod
    def parse():
        args   = sys.argv[1:]
        result = {"flags": [], "options": {}, "args": []}
        i = 0
        while i < len(args):
            a = args[i]
            if a.startswith("--"):
                key = a[2:]
                if i + 1 < len(args) and not args[i+1].startswith("-"):
                    result["options"][key] = args[i+1]
                    i += 1
                else:
                    result["flags"].append(key)
            elif a.startswith("-"):
                result["flags"].append(a[1:])
            else:
                result["args"].append(a)
            i += 1
        return result

    @staticmethod
    def flag(name):
        return name in sys.argv

    @staticmethod
    def option(name, default=None):
        key = f"--{name}"
        if key in sys.argv:
            idx = sys.argv.index(key)
            if idx + 1 < len(sys.argv):
                return sys.argv[idx + 1]
        return default
'''
    }

    code = implementations.get(name, f'# Package: {name}\n')
    with open(os.path.join(pkg_dir, "main.py"), "w") as f:
        f.write(code)

    meta = {
        "name":    name,
        "version": BUILTIN_REGISTRY.get(name, {}).get("version", "1.0.0")
    }
    with open(os.path.join(pkg_dir, "package.json"), "w") as f:
        json.dump(meta, f, indent=2)

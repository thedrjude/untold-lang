import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.lexer.lexer             import Lexer
from src.parser.parser           import Parser
from src.interpreter.interpreter import Interpreter
from cli.config                  import load_config, save_config, init_config, find_project_root
from cli.packages                import pkg_install, pkg_remove, pkg_list, pkg_search, pkg_install_all
from cli.scaffold                import scaffold_project, TEMPLATES

VERSION = "0.1.0"

def cmd_run(filepath, args=None):
    if not filepath:
        # Try entry from untold.json
        cfg = load_config()
        if cfg:
            filepath = cfg.get("entry", "main.ut")
        else:
            print("[Untold] Error: No file specified. Usage: untold run <file.ut>")
            sys.exit(1)

    if not filepath.endswith(".ut"):
        print(f"[Untold] Error: '{filepath}' is not a .ut file")
        sys.exit(1)

    if not os.path.exists(filepath):
        print(f"[Untold] Error: File '{filepath}' not found")
        sys.exit(1)

    with open(filepath, "r") as f:
        source = f.read()

    try:
        tokens = Lexer(source).tokenize()
        ast    = Parser(tokens).parse()
        Interpreter().run(ast)
    except SyntaxError as e:
        print(f"\n[Untold SyntaxError]\n  {e}")
        sys.exit(1)
    except NameError as e:
        print(f"\n[Untold NameError]\n  {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"\n[Untold RuntimeError]\n  {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[Untold Error]\n  {e}")
        sys.exit(1)

def cmd_check(filepath):
    if not filepath or not os.path.exists(filepath):
        print(f"[Untold] Error: File '{filepath}' not found")
        sys.exit(1)

    with open(filepath, "r") as f:
        source = f.read()

    try:
        tokens = Lexer(source).tokenize()
        Parser(tokens).parse()
        print(f"[Untold] OK — '{filepath}' has no syntax errors")
    except SyntaxError as e:
        print(f"[Untold SyntaxError] {e}")
        sys.exit(1)

def cmd_new(args):
    if len(args) < 1:
        print("[Untold] Usage: untold new <name> [template] [--author=...] [--desc=...]")
        print(f"[Untold] Templates: {', '.join(TEMPLATES.keys())}")
        return

    name     = args[0]
    template = args[1] if len(args) > 1 else "app"
    author   = ""
    desc     = ""

    for a in args:
        if a.startswith("--author="):
            author = a.split("=", 1)[1]
        if a.startswith("--desc="):
            desc = a.split("=", 1)[1]

    scaffold_project(template, name, author, desc)

def cmd_init(args):
    name   = args[0] if args else os.path.basename(os.getcwd())
    author = args[1] if len(args) > 1 else ""
    config = init_config(name, author)
    path   = save_config(config)
    print(f"[Untold] Initialized project '{name}'")
    print(f"[Untold] Created {path}")

def cmd_install(args):
    if not args:
        # Install all from untold.json
        cfg = load_config()
        if cfg:
            pkg_install_all(cfg)
            save_config(cfg)
        else:
            print("[utpkg] No untold.json found. Run 'untold init' first.")
        return

    cfg = load_config()
    for pkg in args:
        parts   = pkg.split("@")
        name    = parts[0]
        version = parts[1] if len(parts) > 1 else None
        pkg_install(name, version, cfg)

    if cfg:
        save_config(cfg)

def cmd_remove(args):
    if not args:
        print("[utpkg] Usage: untold remove <package>")
        return
    cfg = load_config()
    for pkg in args:
        pkg_remove(pkg, cfg)
    if cfg:
        save_config(cfg)

def cmd_list_packages():
    pkgs = pkg_list()
    if not pkgs:
        print("[utpkg] No packages installed")
        return
    print(f"\n[utpkg] Installed packages ({len(pkgs)}):")
    for name, version in pkgs:
        print(f"  {name}@{version}")

def cmd_search(args):
    query = args[0] if args else ""
    results = pkg_search(query)
    if not results:
        print(f"[utpkg] No packages found for '{query}'")
        return
    print(f"\n[utpkg] Search results for '{query}':")
    for name, version, desc in results:
        print(f"  {name}@{version} — {desc}")

def cmd_info():
    cfg = load_config()
    if not cfg:
        print("[Untold] No untold.json found in this directory")
        return
    print(f"\n  Project : {cfg.get('name')}")
    print(f"  Version : {cfg.get('version')}")
    print(f"  Author  : {cfg.get('author', '-')}")
    print(f"  Entry   : {cfg.get('entry')}")
    print(f"  Template: {cfg.get('template', '-')}")
    deps = cfg.get("dependencies", {})
    if deps:
        print(f"  Deps    : {', '.join(f'{k}@{v}' for k,v in deps.items())}")
    else:
        print(f"  Deps    : none")

def cmd_run_script(script_name):
    cfg = load_config()
    if not cfg:
        print("[Untold] No untold.json found. Run 'untold init' first.")
        return
    scripts = cfg.get("scripts", {})
    if script_name not in scripts:
        print(f"[Untold] Script '{script_name}' not found in untold.json")
        print(f"[Untold] Available: {', '.join(scripts.keys())}")
        return
    cmd_run(scripts[script_name])

def cmd_version():
    print(f"Untold Lang v{VERSION}")

def cmd_help():
    print(f"""
Untold Lang CLI v{VERSION}

Usage:
  untold <command> [options]

Project commands:
  untold new <name> [template]        Create a new project
  untold init                         Initialize untold.json
  untold info                         Show project info
  untold run [file.ut]                Run an Untold source file
  untold check <file.ut>              Check for syntax errors

Build & compile:
  untold build                        Build project (python script)
  untold build --target binary        Compile to standalone binary
  untold build --target all           Build all targets
  untold build --optimize 2           Max optimization
  untold run-build <name>             Run a built output

Package manager:
  untold install                      Install all deps
  untold install <pkg>                Install a package
  untold remove <pkg>                 Remove a package
  untold list                         List installed packages
  untold search <query>               Search packages

Other:
  untold version                      Show version
  untold help                         Show this help

Examples:
  untold new my-app web
  untold build --target binary
  untold build --target all --optimize 2
  untold install colors uuid
""")
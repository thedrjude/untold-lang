import os
import sys
import shutil
import subprocess
import stat

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.compiler.bundler   import Bundler
from src.compiler.codegen   import CodeGen
from src.compiler.optimizer import Optimizer
from cli.config             import load_config

BUILD_DIR = "dist"

def cmd_build(args):
    # Parse flags
    target    = "python"   # python | binary | exe
    optimize  = 1
    entry     = None
    out_name  = None

    for i, a in enumerate(args):
        if a == "--target" and i+1 < len(args):
            target = args[i+1]
        if a == "--optimize" and i+1 < len(args):
            optimize = int(args[i+1])
        if a == "--out" and i+1 < len(args):
            out_name = args[i+1]
        if a.endswith(".ut"):
            entry = a

    # Load config
    cfg = load_config()
    if not entry:
        entry = cfg.get("entry", "main.ut") if cfg else "main.ut"
    if not out_name:
        out_name = cfg.get("name", "app") if cfg else "app"

    if not os.path.exists(entry):
        print(f"[Untold Build] Entry file '{entry}' not found")
        sys.exit(1)

    os.makedirs(BUILD_DIR, exist_ok=True)

    print(f"[Untold Build] Building '{entry}'...")
    print(f"[Untold Build] Target: {target}")
    print(f"[Untold Build] Optimize: level {optimize}")

    # Step 1 — Bundle
    print(f"[Untold Build] Bundling source files...")
    bundler = Bundler(entry)
    bundled = bundler.bundle()
    print(f"[Untold Build] Bundled {len(bundler.loaded)} file(s)")

    # Step 2 — Optimize
    print(f"[Untold Build] Optimizing...")
    opt    = Optimizer(bundled)
    source = opt.optimize(level=optimize)
    stats  = opt.stats()
    print(f"[Untold Build] Size reduction: {stats['reduction_pct']}%")

    # Step 3 — Generate bootstrap
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gen          = CodeGen(project_root)
    py_out       = os.path.join(BUILD_DIR, f"{out_name}.py")
    gen.generate(source, py_out)
    print(f"[Untold Build] Generated: {py_out}")

    if target == "python":
        _make_executable_script(py_out, out_name)

    elif target == "binary":
        _build_binary(py_out, out_name, platform="linux")

    elif target == "exe":
        _build_binary(py_out, out_name, platform="windows")

    elif target == "all":
        _make_executable_script(py_out, out_name)
        _build_binary(py_out, out_name, platform="linux")

    print(f"\n[Untold Build] Done! Output in ./{BUILD_DIR}/")
    _list_dist()

def _make_executable_script(py_path, name):
    """Make the .py bootstrap directly executable."""
    sh_path = os.path.join(BUILD_DIR, name)
    with open(sh_path, "w") as f:
        f.write(f"#!/usr/bin/env python3\n")
        with open(py_path) as src:
            # Skip the shebang already in py file
            lines = src.readlines()
            f.writelines(lines[1:] if lines[0].startswith("#!") else lines)

    # Make executable
    st = os.stat(sh_path)
    os.chmod(sh_path, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    print(f"[Untold Build] Executable script: {sh_path}")
    return sh_path

def _build_binary(py_path, name, platform="linux"):
    """Use PyInstaller to build a standalone binary."""
    if not shutil.which("pyinstaller"):
        print("[Untold Build] PyInstaller not found.")
        print("[Untold Build] Install it: pip install pyinstaller")
        return False

    print(f"[Untold Build] Compiling to standalone binary with PyInstaller...")

    out_dir  = os.path.join(BUILD_DIR, "bin")
    os.makedirs(out_dir, exist_ok=True)

    cmd = [
        "pyinstaller",
        "--onefile",
        "--clean",
        "--distpath", out_dir,
        "--workpath", os.path.join(BUILD_DIR, ".work"),
        "--specpath", os.path.join(BUILD_DIR, ".spec"),
        "--name",     name,
        "--noconfirm",
        py_path
    ]

    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        binary = os.path.join(out_dir, name)
        if platform == "windows":
            binary += ".exe"
        print(f"[Untold Build] Binary compiled: {binary}")
        return True
    else:
        print(f"[Untold Build] PyInstaller failed with code {result.returncode}")
        return False

def _list_dist():
    print(f"\n[Untold Build] Build output:")
    for root, dirs, files in os.walk(BUILD_DIR):
        # Skip hidden work dirs
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        level   = root.replace(BUILD_DIR, "").count(os.sep)
        indent  = "  " * level
        folder  = os.path.basename(root)
        if level > 0:
            print(f"{indent}{folder}/")
        for f in files:
            size    = os.path.getsize(os.path.join(root, f))
            size_kb = round(size / 1024, 1)
            print(f"{'  ' * (level+1)}{f}  ({size_kb} KB)")

def cmd_run_binary(args):
    """Run a compiled .py bootstrap directly."""
    if not args:
        print("[Untold] Usage: untold run-build <name>")
        return
    path = os.path.join(BUILD_DIR, args[0] + ".py")
    if not os.path.exists(path):
        path = os.path.join(BUILD_DIR, args[0])
    if not os.path.exists(path):
        print(f"[Untold] Built file '{args[0]}' not found in dist/")
        return
    os.execv(sys.executable, [sys.executable, path] + args[1:])
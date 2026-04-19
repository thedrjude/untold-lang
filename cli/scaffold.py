import json
import os

TEMPLATES = {
    "app": {
        "desc": "General purpose Untold Lang app",
        "files": {
            "main.ut": '''\
start main() {
    say("Welcome to {name}!")
    let version = "0.1.0"
    say("Version: " + version)
}
''',
            "lib/utils.ut": '''\
fn greet(name) {
    return "Hello, " + name + "!"
}
''',
            "tests/test.ut": '''\
start main() {
    say("Running tests for {name}...")
    say("All tests passed!")
}
'''
        }
    },
    "web": {
        "desc": "Web server project",
        "files": {
            "main.ut": '''\
use untold.web

start main() {
    say("Starting {name} web server...")
    http.serve(8080)
}
''',
            "routes/index.ut": '''\
fn index_handler(req) {
    return "<h1>Welcome to {name}</h1>"
}
'''
        }
    },
    "ai": {
        "desc": "AI / ML project",
        "files": {
            "main.ut": '''\
use untold.ai
use untold.fs

start main() {
    say("Starting {name} AI project...")
    let text = "Untold Lang AI is powerful and amazing"
    say(ai.sentiment(text))
    say(ai.keywords(text, 5))
}
'''
        }
    },
    "hack": {
        "desc": "Security / ethical hacking toolkit",
        "files": {
            "main.ut": '''\
use untold.hack
use untold.net

start main() {
    say("=== {name} Security Toolkit ===")
    say(hack.sha256("test-target"))
    say(hack.b64_encode("payload"))
}
''',
            "recon/scanner.ut": '''\
use untold.net
use untold.hack

fn scan_target(host) {
    say("Scanning: " + host)
    let ip = hack.resolve(host)
    say("IP: " + ip)
}
'''
        }
    },
    "cli": {
        "desc": "Command line tool",
        "files": {
            "main.ut": '''\
use untold.shell

start main() {
    say("{name} CLI Tool")
    say("Platform: " + shell.platform())
    say("Usage: untold run main.ut [options]")
}
'''
        }
    },
    "script": {
        "desc": "Quick automation script",
        "files": {
            "main.ut": '''\
use untold.shell
use untold.fs

start main() {
    say("Running {name} script...")
    let result = shell.run("echo Script Works!")
    say(result.out)
}
'''
        }
    }
}

def scaffold_project(template, name, author="", description="", path="."):
    if template not in TEMPLATES:
        print(f"[untold] Unknown template '{template}'")
        print(f"[untold] Available: {', '.join(TEMPLATES.keys())}")
        return False

    tpl      = TEMPLATES[template]
    root_dir = os.path.join(path, name)

    if os.path.exists(root_dir):
        print(f"[untold] Directory '{root_dir}' already exists")
        return False

    os.makedirs(root_dir)
    print(f"[untold] Creating {template} project '{name}'...")

    # Write all template files
    for filepath, content in tpl["files"].items():
        full   = os.path.join(root_dir, filepath)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(content.replace("{name}", name))
        print(f"[untold]   created {filepath}")

    # Write untold.json
    config = {
        "name":         name,
        "version":      "0.1.0",
        "description":  description or tpl["desc"],
        "author":       author,
        "license":      "MIT",
        "template":     template,
        "entry":        "main.ut",
        "dependencies": {},
        "scripts": {
            "start": "main.ut",
            "test":  "tests/test.ut"
        }
    }
    with open(os.path.join(root_dir, "untold.json"), "w") as f:
        json.dump(config, f, indent=2)
    print("[untold]   created untold.json")

    # Write .gitignore
    with open(os.path.join(root_dir, ".gitignore"), "w") as f:
        f.write("__pycache__/\n.untold_cache/\n*.pyc\n.env\n")
    print("[untold]   created .gitignore")

    # Write README
    with open(os.path.join(root_dir, "README.md"), "w") as f:
        f.write(f"# {name}\n\n{description or tpl['desc']}\n\n")
        f.write("## Run\n\n```bash\nuntold run main.ut\n```\n\n")
        f.write(f"## Template\n\n`{template}`\n")
    print("[untold]   created README.md")

    print(f"\n[untold] Project '{name}' created successfully!")
    print("[untold] To get started:")
    print(f"           cd {name}")
    print("           untold run main.ut")
    return True

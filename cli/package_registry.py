"""
Untold Lang Package Registry
v2.1.1 - Expanded ecosystem
"""
import json
import os
from pathlib import Path

PACKAGE_REGISTRY = {
    "colors": {
        "version": "1.0.0",
        "description": "Colorful terminal output",
        "author": "untold-lang",
        "module": "colors",
        "source": "https://github.com/untold-lang/untold-colors"
    },
    "uuid": {
        "version": "1.0.0",
        "description": "Generate UUIDs and unique identifiers",
        "author": "untold-lang",
        "module": "uuid",
        "source": "https://github.com/untold-lang/untold-uuid"
    },
    "dotenv": {
        "version": "1.0.0",
        "description": "Environment variable management",
        "author": "untold-lang",
        "module": "dotenv",
        "source": "https://github.com/untold-lang/untold-dotenv"
    },
    "validator": {
        "version": "1.0.0",
        "description": "Data validation utilities",
        "author": "untold-lang",
        "module": "validator",
        "source": "https://github.com/untold-lang/untold-validator"
    },
    "logger": {
        "version": "1.0.0",
        "description": "Advanced logging with levels and formatters",
        "author": "untold-lang",
        "module": "logger",
        "source": "https://github.com/untold-lang/untold-logger"
    },
    "date": {
        "version": "1.0.0",
        "description": "Date and time parsing and formatting",
        "author": "untold-lang",
        "module": "date",
        "source": "https://github.com/untold-lang/untold-date"
    },
    "math": {
        "version": "1.0.0",
        "description": "Extended math operations",
        "author": "untold-lang",
        "module": "math",
        "source": "https://github.com/untold-lang/untold-math"
    },
    "csv": {
        "version": "1.0.0",
        "description": "CSV file parsing and generation",
        "author": "untold-lang",
        "module": "csv",
        "source": "https://github.com/untold-lang/untold-csv"
    },
    "jsonwebtoken": {
        "version": "1.0.0",
        "description": "JWT token generation and verification",
        "author": "untold-lang",
        "module": "jsonwebtoken",
        "source": "https://github.com/untold-lang/untold-jwt"
    },
    "bcrypt": {
        "version": "1.0.0",
        "description": "Password hashing with bcrypt",
        "author": "untold-lang",
        "module": "bcrypt",
        "source": "https://github.com/untold-lang/untold-bcrypt"
    },
    "canvas": {
        "version": "1.0.0",
        "description": "2D graphics and image manipulation",
        "author": "untold-lang",
        "module": "canvas",
        "source": "https://github.com/untold-lang/untold-canvas"
    },
    "pdf": {
        "version": "1.0.0",
        "description": "PDF generation and manipulation",
        "author": "untold-lang",
        "module": "pdf",
        "source": "https://github.com/untold-lang/untold-pdf"
    },
    "yaml": {
        "version": "1.0.0",
        "description": "YAML parsing and serialization",
        "author": "untold-lang",
        "module": "yaml",
        "source": "https://github.com/untold-lang/untold-yaml"
    },
    "websocket": {
        "version": "1.0.0",
        "description": "WebSocket client and server",
        "author": "untold-lang",
        "module": "websocket",
        "source": "https://github.com/untold-lang/untold-websocket"
    },
    "graphql": {
        "version": "1.0.0",
        "description": "GraphQL client",
        "author": "untold-lang",
        "module": "graphql",
        "source": "https://github.com/untold-lang/untold-graphql"
    },
    "compression": {
        "version": "1.0.0",
        "description": "Zip, gzip, and tar compression",
        "author": "untold-lang",
        "module": "compression",
        "source": "https://github.com/untold-lang/untold-compression"
    },
    "email": {
        "version": "1.0.0",
        "description": "Email sending and receiving",
        "author": "untold-lang",
        "module": "email",
        "source": "https://github.com/untold-lang/untold-email"
    },
    "redis": {
        "version": "1.0.0",
        "description": "Redis client for caching",
        "author": "untold-lang",
        "module": "redis",
        "source": "https://github.com/untold-lang/untold-redis"
    },
    "mongo": {
        "version": "1.0.0",
        "description": "MongoDB client",
        "author": "untold-lang",
        "module": "mongo",
        "source": "https://github.com/untold-lang/untold-mongo"
    },
    "cli": {
        "version": "1.0.0",
        "description": "Build CLI applications with ease",
        "author": "untold-lang",
        "module": "cli",
        "source": "https://github.com/untold-lang/untold-cli"
    }
}

class PackageManager:
    def __init__(self):
        self.registry = PACKAGE_REGISTRY
        self.installed = self._load_installed()

    def _load_installed(self):
        installed_path = Path.home() / ".untold" / "packages.json"
        if installed_path.exists():
            with open(installed_path) as f:
                return json.load(f)
        return {}

    def _save_installed(self):
        installed_path = Path.home() / ".untold" / "packages.json"
        installed_path.parent.mkdir(parents=True, exist_ok=True)
        with open(installed_path, "w") as f:
            json.dump(self.installed, f, indent=2)

    def search(self, query):
        results = []
        query = query.lower()
        for name, info in self.registry.items():
            if (query in name or query in info["description"].lower()):
                results.append({"name": name, **info})
        return results

    def install(self, package_name):
        if package_name not in self.registry:
            raise ValueError(f"Package '{package_name}' not found in registry")
        self.installed[package_name] = self.registry[package_name]
        self._save_installed()
        return f"Installed {package_name} v{self.registry[package_name]['version']}"

    def remove(self, package_name):
        if package_name in self.installed:
            del self.installed[package_name]
            self._save_installed()
            return f"Removed {package_name}"
        return f"Package '{package_name}' not installed"

    def list(self):
        return self.installed

    def info(self, package_name):
        if package_name in self.registry:
            return {"name": package_name, **self.registry[package_name]}
        raise ValueError(f"Package '{package_name}' not found")

    def all_packages(self):
        return [{"name": name, **info} for name, info in self.registry.items()]
import os
import re

class Bundler:
    """
    Bundles multiple .ut files into a single source string.
    Resolves 'use' statements that reference local .ut files.
    """

    def __init__(self, entry_path):
        self.entry_path = os.path.abspath(entry_path)
        self.root_dir   = os.path.dirname(self.entry_path)
        self.loaded     = set()
        self.output     = []

    def bundle(self):
        self._load_file(self.entry_path)
        return "\n".join(self.output)

    def _load_file(self, path):
        abs_path = os.path.abspath(path)
        if abs_path in self.loaded:
            return
        self.loaded.add(abs_path)

        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"[Untold Bundler] File not found: {abs_path}")

        with open(abs_path, "r", encoding="utf-8") as f:
            source = f.read()

        for line in source.splitlines():
            stripped = line.strip()
            # Check if it's a local file import: use ./something or use lib/utils
            if stripped.startswith("use ") and not stripped.startswith("use untold."):
                module_path = stripped[4:].strip()
                # Convert module path to file path
                file_path = os.path.join(
                    self.root_dir,
                    module_path.replace(".", os.sep) + ".ut"
                )
                if os.path.exists(file_path):
                    self._load_file(file_path)
                    continue
            self.output.append(line)
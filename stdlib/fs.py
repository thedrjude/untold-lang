import glob
import json
import os
import shutil


class UntoldFS:
    """untold.fs — File system module"""

    @staticmethod
    def read(path):
        with open(path, encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def write(path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(content))

    @staticmethod
    def append(path, content):
        with open(path, "a", encoding="utf-8") as f:
            f.write(str(content))

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def delete(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    @staticmethod
    def copy(src, dst):
        shutil.copy2(src, dst)

    @staticmethod
    def move(src, dst):
        shutil.move(src, dst)

    @staticmethod
    def mkdir(path):
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def listdir(path="."):
        return os.listdir(path)

    @staticmethod
    def isfile(path):
        return os.path.isfile(path)

    @staticmethod
    def isdir(path):
        return os.path.isdir(path)

    @staticmethod
    def size(path):
        return os.path.getsize(path)

    @staticmethod
    def basename(path):
        return os.path.basename(path)

    @staticmethod
    def dirname(path):
        return os.path.dirname(path)

    @staticmethod
    def join(*parts):
        return os.path.join(*parts)

    @staticmethod
    def glob(pattern):
        return glob.glob(pattern, recursive=True)

    @staticmethod
    def read_json(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def write_json(path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def cwd():
        return os.getcwd()

    @staticmethod
    def abspath(path):
        return os.path.abspath(path)

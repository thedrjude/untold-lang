import subprocess
import os
import sys
import platform

class UntoldShell:
    """untold.shell — Scripting & system module"""

    @staticmethod
    def run(cmd, capture=True):
        result = subprocess.run(
            cmd, shell=True,
            capture_output=capture,
            text=True
        )
        return {
            "out":  result.stdout.strip(),
            "err":  result.stderr.strip(),
            "code": result.returncode,
            "ok":   result.returncode == 0
        }

    @staticmethod
    def run_live(cmd):
        """Run command and print output in real time."""
        proc = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        output = []
        for line in proc.stdout:
            print(line, end="")
            output.append(line)
        proc.wait()
        return {
            "out":  "".join(output),
            "code": proc.returncode,
            "ok":   proc.returncode == 0
        }

    @staticmethod
    def env(key, default=None):
        return os.environ.get(key, default)

    @staticmethod
    def set_env(key, value):
        os.environ[key] = str(value)

    @staticmethod
    def platform():
        return platform.system().lower()   # "linux", "windows", "darwin"

    @staticmethod
    def arch():
        return platform.machine()

    @staticmethod
    def python_version():
        return sys.version

    @staticmethod
    def exit(code=0):
        sys.exit(code)

    @staticmethod
    def which(cmd):
        import shutil
        return shutil.which(cmd)

    @staticmethod
    def pid():
        return os.getpid()

    @staticmethod
    def hostname():
        import socket
        return socket.gethostname()

    @staticmethod
    def args():
        return sys.argv[1:]
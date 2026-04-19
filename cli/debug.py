"""
Untold Lang - Debugger
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter


class Debugger:
    """Step-through debugger"""

    def __init__(self, source):
        self.source = source
        self.tokens = Lexer(source).tokenize()
        self.ast = Parser(self.tokens).parse()
        self.interpreter = Interpreter()
        self.line = 1
        self.bp = set()

    def run(self):
        """Run with debugging enabled"""
        print(f"[Debug] Untold Lang Debugger v2.0.0")
        print(f"[Debug] {len(self.ast.statements)} statements")
        print("[Debug] Type 'help' for commands")
        print()

        while True:
            try:
                print(f"untold:{self.line}> ", end="")
                cmd = input().strip().split()

                if not cmd:
                    continue

                if cmd[0] == "quit":
                    print("Debug session ended")
                    break

                if cmd[0] == "help":
                    print("Commands:")
                    print("  run     - Execute all remaining")
                    print("  step    - Execute next statement")
                    print("  next    - Same as step")
                    print("  break n - Set breakpoint at line n")
                    print("  clear n - Clear breakpoint at line n")
                    print("  list   - Show source code")
                    print("  vars   - Show variables")
                    print("  quit   - Exit debugger")
                    continue

                if cmd[0] == "run":
                    print("[Debug] Running to completion...")
                    try:
                        result = self.interpreter.run(self.ast)
                        if result:
                            print(f"Result: {result}")
                    except Exception as e:
                        print(f"Error: {e}")
                    break

                if cmd[0] in ("step", "next"):
                    print(f"[Debug] Stepping to line {self.line + 1}...")
                    print("[Debug] (Step execution not fully implemented - use 'run')")
                    continue

                if cmd[0] == "list":
                    lines = self.source.split("\n")
                    for i, line in enumerate(lines, 1):
                        marker = "*" if i == self.line else " "
                        print(f" {marker} {i:3}: {line}")
                    continue

                if cmd[0] == "vars":
                    print(f"[Debug] Globals: {list(self.interpreter.globals.data.keys())}")
                    continue

            except KeyboardInterrupt:
                print("\n[Debug] Use 'quit' to exit")
            except EOFError:
                break


def cmd_debug(source_file):
    """Start debugger"""
    if not source_file:
        print("[Debug] Usage: untold debug <file.ut>")
        return

    try:
        with open(source_file) as f:
            source = f.read()
        dbg = Debugger(source)
        dbg.run()
    except FileNotFoundError:
        print(f"[Debug] File not found: {source_file}")
    except Exception as e:
        print(f"[Debug] Error: {e}")
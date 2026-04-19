"""
Untold Lang - Interactive REPL
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter


def cmd_repl():
    """Start interactive REPL"""
    print(f"Untold Lang v2.0.0 — Interactive Mode")
    print("Type '.help' for commands, '.exit' to quit")
    print()

    interpreter = Interpreter()
    env = {}

    while True:
        try:
            code = input(">> ").strip()

            if not code:
                continue

            if code == ".exit":
                print("Goodbye!")
                break

            if code == ".help":
                print("REPL Commands:")
                print("  .exit     - Exit REPL")
                print("  .help    - Show this help")
                print("  .clear   - Clear environment")
                print("  .vars    - Show variables")
                print("  .reset   - Reset REPL state")
                continue

            if code == ".clear":
                env = {}
                interpreter = Interpreter()
                print("Environment cleared")
                continue

            if code == ".vars":
                print(f"Variables: {env}")
                continue

            if code == ".reset":
                interpreter = Interpreter()
                env = {}
                print("REPL reset")
                continue

            # Execute the code
            try:
                tokens = Lexer(code).tokenize()
                ast = Parser(tokens).parse()
                result = interpreter.run(ast)

                if result is not None:
                    print(result)
            except Exception as e:
                print(f"Error: {e}")

        except KeyboardInterrupt:
            print("\nUse .exit to quit")
        except EOFError:
            print("\nGoodbye!")
            break
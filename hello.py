"""§3.1 — a plain script to run inside VS Code and verify the interpreter."""
import sys

print("Hello from the isolated environment.")
print("Interpreter:", sys.executable)  # must resolve inside .venv (§3.2)

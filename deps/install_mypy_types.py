import subprocess

subprocess.run(["mypy", ".", "--check-untyped-defs"])
subprocess.run(["mypy", "--install-types", "--non-interactive"])

import subprocess
import sys

subprocess.run(
    ["mypy", ".", "--check-untyped-defs", *sys.argv[1:]],
    check=True,
    shell=True,
)

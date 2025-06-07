import subprocess

subprocess.run(
    ["mypy", ".", "--check-untyped-defs"],
    check=True,
    shell=True,
)

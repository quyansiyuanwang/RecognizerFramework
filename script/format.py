import subprocess

subprocess.run(["black", "**/*.py"], check=True, shell=True)

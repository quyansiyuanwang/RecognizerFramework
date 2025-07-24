import subprocess

subprocess.run(
    ["pip", "install", "-r", "deps/requirements.txt"], check=True, shell=True
)

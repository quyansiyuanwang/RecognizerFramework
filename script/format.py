import subprocess
import sys

subprocess.run(["black", "**/*.py", *sys.argv[1:]], check=True, shell=True)

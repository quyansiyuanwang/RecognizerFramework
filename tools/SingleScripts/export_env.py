import re
import subprocess

# conda export
subprocess.run(
    ["conda", "env", "export", "--file", "deps/environment.yml"],
    check=True,
)
with open("deps/environment.yml", "r+") as f:
    content = f.read()
    # remove the prefix line
    pattern = r"^prefix: .*\n?"
    content = re.sub(pattern, "", content, flags=re.MULTILINE)
    f.seek(0)
    f.write(content)
    f.truncate()


# pip freeze
subprocess.run(
    ["pip", "freeze"],
    stdout=open("deps/requirements.txt", "w"),
    check=True,
)

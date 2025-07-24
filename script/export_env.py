import subprocess
import re


# conda export
subprocess.run(
    ["conda", "env", "export", "--file", "./environment.yml"],
    check=True,
)
with open("./environment.yml", "r+") as f:
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
    stdout=open("requirements.txt", "w"),
    check=True,
)

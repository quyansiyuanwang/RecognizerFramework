import subprocess
import sys
from typing import List


def get_changed_files(base_ref: str, head_ref: str):
    cmd = ["git", "diff", "--name-only", f"{base_ref}", f"{head_ref}"]
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return files


def only_md_files(files: List[str]) -> bool:
    return all(f.lower().endswith(".md") for f in files)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python diff_only_docs.py <base_ref> <head_ref>")
        sys.exit(2)
    base_ref = sys.argv[1]
    head_ref = sys.argv[2]
    files = get_changed_files(base_ref, head_ref)
    if not files:
        print("no-changes")
        sys.exit(0)
    if only_md_files(files):
        print("only-md")
        sys.exit(0)
    else:
        print("not-only-md")
        sys.exit(1)

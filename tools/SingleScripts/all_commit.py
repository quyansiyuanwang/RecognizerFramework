import subprocess


def git_add_commit():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit"], check=True)
        print("Changes added and committed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    git_add_commit()

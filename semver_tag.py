# semver_tag.py
import semver
import subprocess

def get_latest_tag():
    try:
        return subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).strip().decode()
    except subprocess.CalledProcessError:
        return '0.0.0'

def bump_minor(tag):
    parsed = semver.VersionInfo.parse(tag)
    return str(parsed.bump_minor())

if __name__ == "__main__":
    latest = get_latest_tag()
    new_tag = bump_minor(latest)
    subprocess.run(['git', 'tag', new_tag])
    subprocess.run(['git', 'push', 'origin', new_tag])
    print(f"::set-output name=version::{new_tag}")

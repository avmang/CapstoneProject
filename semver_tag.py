import semver
import subprocess
import os

def get_latest_tag():
    try:
        tag = subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0'],
            stderr=subprocess.DEVNULL
        ).strip().decode()
    except subprocess.CalledProcessError:
        tag = '0.0.0'
    return tag

def bump_minor(tag):
    parsed = semver.VersionInfo.parse(tag)
    return str(parsed.bump_minor())

if __name__ == "__main__":
    latest_tag = get_latest_tag()
    new_version = bump_minor(latest_tag)

    output_path = os.environ.get('GITHUB_OUTPUT')
    if output_path:
        with open(output_path, 'a') as f:
            f.write(f"version={new_version}\n")

    print(new_version)

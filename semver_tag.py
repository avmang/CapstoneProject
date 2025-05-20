import semver
import subprocess
import os
import sys

def get_latest_tag():
    try:
        tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).strip().decode()
    except subprocess.CalledProcessError:
        tag = '0.0.0'
    return tag

def bump_minor(tag):
    parsed = semver.VersionInfo.parse(tag)
    return str(parsed.bump_minor())

def run_git_command(args):
    result = subprocess.run(args, check=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

if __name__ == "__main__":
    latest = get_latest_tag()
    new_tag = bump_minor(latest)

    run_git_command(['git', 'config', 'user.name', 'github-actions'])
    run_git_command(['git', 'config', 'user.email', 'github-actions@github.com'])

    run_git_command(['git', 'tag', new_tag])
    run_git_command(['git', 'push', 'origin', new_tag])

    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f"version={new_tag}", file=fh)
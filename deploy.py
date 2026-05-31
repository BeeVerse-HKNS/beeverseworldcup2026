import subprocess
import shutil
import argparse
import time
import urllib.request
import urllib.error
from pathlib import Path

SRC_DIR = Path(r'd:\My_Code_Projects\Harnessing\projects\world-2026')
DEPLOY_DIR = Path(r'd:\My_Code_Projects\Harnessing\projects\world-2026-deploy')

EXCLUDE_FILES = {'deploy.py', '__pycache__', 'data', '.git'}

VERSIONS = {
    'beeverse': {
        'version_config.py': 'APP_VERSION = "china"\n',
        '.streamlit/secrets.toml': 'APP_VERSION = "china"\n',
        'commit_msg': 'deploy: china version',
        'url': 'https://beeverseworldcup2026.streamlit.app/',
        'remotes': ['beeverse', 'origin'],
    },
    'intl': {
        'version_config.py': 'APP_VERSION = "international"\n',
        '.streamlit/secrets.toml': 'APP_VERSION = "international"\n',
        'commit_msg': 'deploy: international version',
        'url': 'https://beeverse-wc2026-international.streamlit.app/',
        'remotes': ['intl'],
    },
}

HEALTH_CHECK_RETRIES = 5
HEALTH_CHECK_INTERVAL = 30


def run_git(*args, check=True):
    result = subprocess.run(
        ['git'] + list(args),
        cwd=str(DEPLOY_DIR),
        capture_output=True,
        text=True,
        check=check,
    )
    return result


def sync_source_files():
    print('Syncing source files...')
    for item in SRC_DIR.iterdir():
        if item.name in EXCLUDE_FILES or item.name.startswith('.'):
            continue
        if item.is_file():
            shutil.copy2(str(item), str(DEPLOY_DIR / item.name))
        elif item.is_dir():
            dst = DEPLOY_DIR / item.name
            if dst.exists():
                shutil.rmtree(str(dst))
            shutil.copytree(str(item), str(dst))

    secrets_src = SRC_DIR / '.streamlit' / 'secrets.toml'
    secrets_dst = DEPLOY_DIR / '.streamlit' / 'secrets.toml'
    if secrets_src.exists():
        shutil.copy2(str(secrets_src), str(secrets_dst))

    print('Source files synced.')


def write_version_files(version_key):
    config = VERSIONS[version_key]
    for rel_path, content in config.items():
        if rel_path in ('commit_msg', 'url', 'remotes'):
            continue
        target = DEPLOY_DIR / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')
        print(f'  Written: {rel_path} = {content.strip()}')


def health_check(version_key):
    url = VERSIONS[version_key]['url']
    print(f'\nHealth check for {version_key}: {url}')

    for attempt in range(1, HEALTH_CHECK_RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'deploy-health-check/1.0'})
            resp = urllib.request.urlopen(req, timeout=15)
            status = resp.getcode()
            if 200 <= status < 400:
                print(f'  Attempt {attempt}/{HEALTH_CHECK_RETRIES}: OK (HTTP {status})')
                return True
        except urllib.error.HTTPError as e:
            if 200 <= e.code < 400:
                print(f'  Attempt {attempt}/{HEALTH_CHECK_RETRIES}: OK (HTTP {e.code})')
                return True
            print(f'  Attempt {attempt}/{HEALTH_CHECK_RETRIES}: HTTP {e.code}')
        except Exception as e:
            print(f'  Attempt {attempt}/{HEALTH_CHECK_RETRIES}: {type(e).__name__} - {e}')

        if attempt < HEALTH_CHECK_RETRIES:
            print(f'  Waiting {HEALTH_CHECK_INTERVAL}s before retry...')
            time.sleep(HEALTH_CHECK_INTERVAL)

    print(f'  Health check FAILED after {HEALTH_CHECK_RETRIES} attempts.')
    return False


def deploy_version(version_key):
    config = VERSIONS[version_key]
    print(f'\nDeploying to {version_key}...')

    write_version_files(version_key)

    run_git('add', '-A')
    run_git('commit', '-m', config['commit_msg'])

    remotes = config.get('remotes', [version_key])
    for remote in remotes:
        print(f'  Pushing to {remote}...')
        run_git('push', remote, 'main')

    print(f'Deployed to {version_key} successfully!')


def print_summary(results):
    print('\n' + '=' * 50)
    print('DEPLOYMENT SUMMARY')
    print('=' * 50)
    for version_key, info in results.items():
        deploy_status = info.get('deploy', 'skipped')
        health_status = info.get('health', 'skipped')
        url = VERSIONS[version_key]['url']
        print(f'  {version_key}:')
        print(f'    Deploy: {deploy_status}')
        print(f'    Health: {health_status}')
        print(f'    URL:    {url}')
    print('=' * 50)


def parse_args():
    parser = argparse.ArgumentParser(description='Deploy World 2026 app to Streamlit Cloud')
    parser.add_argument('--verify-only', action='store_true', help='Only run health checks without deploying')
    parser.add_argument('--version', choices=list(VERSIONS.keys()), help='Deploy only a specific version')
    return parser.parse_args()


def main():
    args = parse_args()
    results = {}
    target_versions = [args.version] if args.version else list(VERSIONS.keys())

    if args.verify_only:
        print('Verify-only mode: skipping deployment, running health checks...')
        for version_key in target_versions:
            ok = health_check(version_key)
            results[version_key] = {
                'deploy': 'skipped',
                'health': 'OK' if ok else 'FAILED',
            }
        print_summary(results)
        return

    sync_source_files()

    run_git('add', '-A')
    try:
        run_git('commit', '-m', 'chore: sync source files')
    except subprocess.CalledProcessError:
        print('No changes to commit from sync.')

    for version_key in target_versions:
        deploy_version(version_key)
        ok = health_check(version_key)
        results[version_key] = {
            'deploy': 'OK',
            'health': 'OK' if ok else 'FAILED',
        }

    print('\nResetting deploy dir to international (default)...')
    write_version_files('intl')
    run_git('add', '-A')
    try:
        run_git('commit', '-m', 'chore: reset to international default')
    except subprocess.CalledProcessError:
        print('No changes to reset.')

    print_summary(results)


if __name__ == '__main__':
    main()

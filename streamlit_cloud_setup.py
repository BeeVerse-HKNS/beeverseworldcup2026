import argparse
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

SCREENSHOT_DIR = Path(r'd:\My_Code_Projects\Harnessing\projects\world-2026\deploy_screenshots')

APPS = {
    'china': {
        'url': 'https://beeverseworldcup2026.streamlit.app/',
        'repo': 'BeeVerse-HKNS/beeverseworldcup2026',
        'branch': 'main',
        'main_file': 'streamlit_app.py',
    },
    'intl': {
        'url': 'https://wc2026-international.streamlit.app/',
        'repo': 'BeeVerse-HKNS/wc2026-international',
        'branch': 'main',
        'main_file': 'streamlit_app.py',
    },
}

APP_LOAD_TIMEOUT = 60000

DEPLOY_WAIT_TIMEOUT = 30000


def ensure_browsers():
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'playwright', 'install', '--dry-run', 'chromium'],
            capture_output=True, text=True,
        )
        if result.returncode != 0 or 'not installed' in (result.stdout + result.stderr).lower():
            print('Chromium browser not found. Installing...')
            subprocess.run([sys.executable, '-m', 'playwright', 'install', 'chromium'], check=True)
            print('Chromium installed.')
        else:
            print('Chromium browser already installed.')
    except Exception:
        print('Could not verify browser installation. Attempting install...')
        subprocess.run([sys.executable, '-m', 'playwright', 'install', 'chromium'], check=True)
        print('Chromium installed.')


def take_screenshot(page, name):
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    filepath = SCREENSHOT_DIR / f'{name}_{timestamp}.png'
    page.screenshot(path=str(filepath), full_page=True)
    print(f'  Screenshot saved: {filepath}')
    return filepath


def check_app(url, version_key):
    print(f'\nChecking app [{version_key}]: {url}')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()

        try:
            page.goto(url, wait_until='domcontentloaded', timeout=APP_LOAD_TIMEOUT)

            try:
                page.wait_for_selector(
                    '[data-testid="stAppViewContainer"], .stApp, main, [data-testid="stSidebar"]',
                    timeout=APP_LOAD_TIMEOUT,
                )
            except PlaywrightTimeout:
                pass

            time.sleep(3)
            take_screenshot(page, f'check_{version_key}')

            body_text = page.inner_text('body').lower()
            error_indicators = [
                '404', 'not found', 'error', 'something went wrong',
                'connection refused', 'unable to connect', 'this site can\'t be reached',
                'app not found', 'streamlit community cloud',
            ]
            has_error = any(indicator in body_text for indicator in error_indicators)

            if has_error:
                print(f'  Result: APP MAY HAVE ISSUES (error indicators found)')
                return False

            print(f'  Result: APP APPEARS WORKING')
            return True

        except PlaywrightTimeout:
            print(f'  Result: TIMEOUT waiting for app to load')
            take_screenshot(page, f'check_{version_key}_timeout')
            return False
        except Exception as e:
            print(f'  Result: ERROR - {type(e).__name__}: {e}')
            try:
                take_screenshot(page, f'check_{version_key}_error')
            except Exception:
                pass
            return False
        finally:
            browser.close()


def create_app(repo_url, app_name, version_key):
    config = APPS[version_key]
    print(f'\nCreating app [{version_key}]: {config["repo"]}')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()

        try:
            page.goto('https://share.streamlit.io/', wait_until='domcontentloaded', timeout=30000)
            time.sleep(3)

            login_required = False
            try:
                page.wait_for_selector('text=Log in', timeout=5000)
                login_required = True
            except PlaywrightTimeout:
                pass

            try:
                page.wait_for_selector('text=Sign in', timeout=3000)
                login_required = True
            except PlaywrightTimeout:
                pass

            if login_required:
                print('  Login required. Please log in with your GitHub account in the browser window.')
                print('  Waiting for login to complete...')
                try:
                    page.wait_for_url('**/share.streamlit.io/**', timeout=120000)
                except PlaywrightTimeout:
                    try:
                        page.wait_for_selector('text=New app', timeout=10000)
                    except PlaywrightTimeout:
                        print('  Login may not have completed. Continuing anyway...')
                time.sleep(3)

            take_screenshot(page, f'create_{version_key}_loggedin')

            new_app_clicked = False
            selectors = [
                'text=New app',
                'text=Create app',
                'button:has-text("New")',
                'a:has-text("New app")',
                '[data-testid="new-app-button"]',
            ]
            for selector in selectors:
                try:
                    el = page.wait_for_selector(selector, timeout=5000)
                    if el:
                        el.click()
                        new_app_clicked = True
                        print(f'  Clicked "New app" button')
                        break
                except PlaywrightTimeout:
                    continue

            if not new_app_clicked:
                print('  Could not find "New app" button. Taking screenshot for debugging.')
                take_screenshot(page, f'create_{version_key}_no_button')
                return False

            time.sleep(3)
            take_screenshot(page, f'create_{version_key}_form')

            repo_selectors = [
                'input[placeholder*="repository" i]',
                'input[placeholder*="repo" i]',
                'input[aria-label*="repository" i]',
                'input[aria-label*="Repo" i]',
                'input[name*="repo" i]',
                '#repository',
            ]
            repo_filled = False
            for selector in repo_selectors:
                try:
                    el = page.wait_for_selector(selector, timeout=5000)
                    if el:
                        el.fill(config['repo'])
                        repo_filled = True
                        print(f'  Filled repository: {config["repo"]}')
                        break
                except PlaywrightTimeout:
                    continue

            if not repo_filled:
                try:
                    inputs = page.query_selector_all('input[type="text"], input:not([type])')
                    for inp in inputs:
                        placeholder = inp.get_attribute('placeholder') or ''
                        aria_label = inp.get_attribute('aria-label') or ''
                        if 'repo' in placeholder.lower() or 'repo' in aria_label.lower():
                            inp.fill(config['repo'])
                            repo_filled = True
                            print(f'  Filled repository (fallback): {config["repo"]}')
                            break
                except Exception:
                    pass

            if not repo_filled:
                print('  Could not find repository input field.')
                take_screenshot(page, f'create_{version_key}_no_repo_field')
                return False

            time.sleep(1)

            branch_selectors = [
                'input[placeholder*="branch" i]',
                'input[aria-label*="branch" i]',
                'input[name*="branch" i]',
                '#branch',
                'select[name*="branch" i]',
            ]
            for selector in branch_selectors:
                try:
                    el = page.wait_for_selector(selector, timeout=3000)
                    if el:
                        tag = el.evaluate('el => el.tagName.toLowerCase()')
                        if tag == 'select':
                            el.select_option(label=config['branch'])
                        else:
                            el.fill(config['branch'])
                        print(f'  Set branch: {config["branch"]}')
                        break
                except PlaywrightTimeout:
                    continue

            time.sleep(1)

            main_file_selectors = [
                'input[placeholder*="main file" i]',
                'input[placeholder*="file path" i]',
                'input[aria-label*="main file" i]',
                'input[aria-label*="file" i]',
                'input[name*="file" i]',
                '#filePath',
                '#mainFile',
            ]
            for selector in main_file_selectors:
                try:
                    el = page.wait_for_selector(selector, timeout=3000)
                    if el:
                        el.fill(config['main_file'])
                        print(f'  Set main file: {config["main_file"]}')
                        break
                except PlaywrightTimeout:
                    continue

            time.sleep(1)
            take_screenshot(page, f'create_{version_key}_filled')

            deploy_clicked = False
            deploy_selectors = [
                'button:has-text("Deploy")',
                'input[type="submit"][value*="Deploy" i]',
                'button:has-text("Create")',
                'button[type="submit"]',
            ]
            for selector in deploy_selectors:
                try:
                    el = page.wait_for_selector(selector, timeout=5000)
                    if el:
                        el.click()
                        deploy_clicked = True
                        print(f'  Clicked deploy button')
                        break
                except PlaywrightTimeout:
                    continue

            if not deploy_clicked:
                print('  Could not find deploy button.')
                take_screenshot(page, f'create_{version_key}_no_deploy')
                return False

            print('  Waiting for deployment to start...')
            time.sleep(5)
            take_screenshot(page, f'create_{version_key}_deploying')

            print(f'  App creation initiated for {version_key}.')
            print(f'  Monitor the deployment at: https://share.streamlit.io/')
            return True

        except PlaywrightTimeout:
            print(f'  TIMEOUT during app creation')
            take_screenshot(page, f'create_{version_key}_timeout')
            return False
        except Exception as e:
            print(f'  ERROR - {type(e).__name__}: {e}')
            try:
                take_screenshot(page, f'create_{version_key}_error')
            except Exception:
                pass
            return False
        finally:
            browser.close()


def check_versions(versions):
    results = {}
    for v in versions:
        config = APPS[v]
        ok = check_app(config['url'], v)
        results[v] = 'OK' if ok else 'FAILED'
    print_summary(results, 'CHECK')
    return results


def create_versions(versions):
    results = {}
    for v in versions:
        config = APPS[v]
        ok = create_app(config['url'], config['repo'], v)
        results[v] = 'OK' if ok else 'FAILED'
    print_summary(results, 'CREATE')
    return results


def full_setup():
    print('=' * 50)
    print('FULL SETUP: Check existing apps, create missing ones')
    print('=' * 50)

    check_results = check_versions(list(APPS.keys()))

    missing = [v for v, status in check_results.items() if status == 'FAILED']

    if missing:
        print(f'\nMissing/failed apps: {missing}')
        print('Creating missing apps...')
        create_results = create_versions(missing)
    else:
        print('\nAll apps are working. No creation needed.')
        create_results = {}

    print('\n' + '=' * 50)
    print('FULL SETUP SUMMARY')
    print('=' * 50)
    for v in APPS:
        check_status = check_results.get(v, 'skipped')
        create_status = create_results.get(v, 'not needed')
        print(f'  {v}:')
        print(f'    Check:  {check_status}')
        print(f'    Create: {create_status}')
        print(f'    URL:    {APPS[v]["url"]}')
    print('=' * 50)


def print_summary(results, label):
    print(f'\n{"=" * 50}')
    print(f'{label} SUMMARY')
    print(f'{"=" * 50}')
    for v, status in results.items():
        print(f'  {v}: {status}  ({APPS[v]["url"]})')
    print(f'{"=" * 50}')


def parse_args():
    parser = argparse.ArgumentParser(description='Streamlit Cloud app creation and verification')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    check_parser = subparsers.add_parser('check', help='Check if Streamlit Cloud apps are working')
    check_parser.add_argument('--version', choices=['china', 'intl'], help='Check only a specific version')

    create_parser = subparsers.add_parser('create', help='Create a Streamlit Cloud app')
    create_parser.add_argument('--version', choices=['china', 'intl'], required=True, help='Which version to create')

    subparsers.add_parser('setup', help='Full setup: check both, create missing ones')

    return parser.parse_args()


def main():
    args = parse_args()

    if not args.command:
        print('No command specified. Use "check", "create", or "setup".')
        print('Run with --help for usage information.')
        sys.exit(1)

    ensure_browsers()

    if args.command == 'check':
        versions = [args.version] if args.version else list(APPS.keys())
        check_versions(versions)
    elif args.command == 'create':
        create_versions([args.version])
    elif args.command == 'setup':
        full_setup()


if __name__ == '__main__':
    main()

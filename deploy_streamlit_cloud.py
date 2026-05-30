import os
import time
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = r"d:\My_Code_Projects\Harnessing\projects\world-2026\deploy_screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

USER_DATA_DIR = r"d:\My_Code_Projects\Harnessing\projects\world-2026\.browser_data"
os.makedirs(USER_DATA_DIR, exist_ok=True)

REPO = "BeeVerse-HKNS/wc2026-international"
BRANCH = "main"
MAIN_FILE = "streamlit_app.py"
APP_NAME = "wc2026-international"

result = {"success": False, "url": None, "error": None}


def save_screenshot(page, filename):
    path = os.path.join(SCREENSHOT_DIR, filename)
    page.screenshot(path=path, full_page=False)
    print(f"[Screenshot] Saved: {path}")
    return path


def find_element(page, selectors, timeout=10000):
    for sel in selectors:
        try:
            el = page.wait_for_selector(sel, timeout=timeout)
            if el:
                return el
        except Exception:
            continue
    return None


def find_and_click(page, selectors, timeout=10000):
    el = find_element(page, selectors, timeout=timeout)
    if el:
        el.click()
        return True
    return None


def is_logged_in_streamlit(page):
    try:
        body_text = page.inner_text("body").lower()
    except Exception:
        return False

    logged_out_indicators = [
        "continue to sign-in",
        "sign in with github",
        "log in to continue",
    ]
    for indicator in logged_out_indicators:
        if indicator in body_text:
            return False

    logged_in_indicators = [
        "new app",
        "my apps",
        "your apps",
        "workspace",
        "create app",
        "deploy",
    ]
    for indicator in logged_in_indicators:
        if indicator in body_text:
            return True

    return False


with sync_playwright() as p:
    browser = None
    try:
        print("[Step 1] Launching browser with persistent context...")
        context = p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--start-maximized"],
        )
        page = context.new_page()

        print("[Step 2] Navigating to https://share.streamlit.io/ ...")
        page.goto("https://share.streamlit.io/", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(5)

        print("[Step 5] Taking landing page screenshot...")
        save_screenshot(page, "streamlit_cloud_landing.png")

        current_url = page.url
        print(f"[Step 6] Current URL: {current_url}")

        logged_in = is_logged_in_streamlit(page)
        print(f"[Step 6] Logged in: {logged_in}")

        if not logged_in:
            print("[Step 6a] Clicking 'Continue to sign-in'...")
            continue_selectors = [
                "button:has-text('Continue to sign-in')",
                "button:has-text('Sign in')",
                "a:has-text('Sign in')",
            ]
            clicked = find_and_click(page, continue_selectors, timeout=10000)
            if clicked:
                print("[Step 6b] Clicked sign-in button. Waiting for OAuth redirect...")
                time.sleep(5)
                try:
                    page.wait_for_load_state("domcontentloaded", timeout=15000)
                except Exception:
                    pass
                save_screenshot(page, "streamlit_cloud_after_signin_click.png")
                print(f"  Current URL: {page.url}")

                if "authkit.streamlit.io" in page.url:
                    print("[Step 6c] On authkit page. Looking for GitHub login button...")
                    time.sleep(3)
                    github_selectors = [
                        "button:has-text('Continue with GitHub')",
                        "button:has-text('GitHub')",
                        "a:has-text('Continue with GitHub')",
                        "a:has-text('GitHub')",
                        "button:has-text('Sign in with GitHub')",
                        "[data-testid='github-login']",
                        "button:has-text('Continue')",
                    ]
                    github_clicked = find_and_click(page, github_selectors, timeout=15000)
                    if github_clicked:
                        print("[Step 6d] Clicked GitHub login on authkit page!")
                        time.sleep(5)
                        try:
                            page.wait_for_load_state("domcontentloaded", timeout=15000)
                        except Exception:
                            pass
                        save_screenshot(page, "streamlit_cloud_after_github_click.png")
                        print(f"  Current URL: {page.url}")
                    else:
                        print("[Step 6d] Could not find GitHub button on authkit page")
                        buttons_on_authkit = page.query_selector_all("button")
                        for i, btn in enumerate(buttons_on_authkit):
                            try:
                                text = btn.inner_text().strip()
                                if btn.is_visible() and text:
                                    print(f"  Authkit Button: '{text[:100]}'")
                            except Exception:
                                pass

            print("=" * 60)
            print("NOT LOGGED IN - Please log in with your GitHub account")
            print("(BeeVerse-HKNS) in the browser window")
            print("The browser will remember your login for next time.")
            print("=" * 60)

            print("[Step 7] Waiting up to 300s for login...")
            login_wait_start = time.time()
            login_success = False
            while time.time() - login_wait_start < 300:
                time.sleep(5)
                current_url = page.url
                if "share.streamlit.io" in current_url and "authkit" not in current_url and "login" not in current_url:
                    time.sleep(3)
                    try:
                        has_continue = page.query_selector("button:has-text('Continue to sign-in')")
                        if not has_continue:
                            login_success = True
                            print("[Login] Back on Streamlit, no login prompt - logged in!")
                            break
                    except Exception:
                        pass
                    if is_logged_in_streamlit(page):
                        login_success = True
                        print("[Login] Successfully logged in!")
                        break
                if "github.com" in current_url:
                    print(f"[Login] On GitHub - please authorize... ({int(time.time() - login_wait_start)}s)")
                elif "authkit" in current_url:
                    print(f"[Login] On authkit - please complete login... ({int(time.time() - login_wait_start)}s)")
                else:
                    elapsed = int(time.time() - login_wait_start)
                    print(f"[Login] Still waiting... URL={current_url[:60]} ({elapsed}s / 300s)")

            if not login_success:
                save_screenshot(page, "streamlit_cloud_login_timeout.png")
                raise Exception("Login timeout after 300 seconds")
        else:
            print("[Step 6] Already logged in!")

        time.sleep(3)
        page.wait_for_load_state("networkidle", timeout=30000)
        save_screenshot(page, "streamlit_cloud_logged_in.png")

        print(f"[Step 8] Current URL: {page.url}")

        print("[Step 8b] Dumping page elements for debug...")
        buttons = page.query_selector_all("button")
        for i, btn in enumerate(buttons):
            try:
                text = btn.inner_text().strip()
                if btn.is_visible() and text:
                    print(f"  Visible Button: '{text[:100]}'")
            except Exception:
                pass

        links = page.query_selector_all("a")
        for i, link in enumerate(links):
            try:
                text = link.inner_text().strip()
                href = link.get_attribute("href") or ""
                if link.is_visible() and text:
                    print(f"  Visible Link: '{text[:80]}' href='{href[:100]}'")
            except Exception:
                pass

        print("[Step 8c] Looking for 'Create app' / 'New app' button...")
        new_app_selectors = [
            "button:has-text('Create app')",
            "a:has-text('Create app')",
            "button:has-text('New app')",
            "a:has-text('New app')",
            "text=Create app",
            "text=New app",
            "button:has-text('Deploy')",
            "a:has-text('Deploy')",
            "[data-testid='new-app-button']",
        ]
        clicked_new_app = find_and_click(page, new_app_selectors, timeout=15000)

        if not clicked_new_app:
            print("[Step 8d] Trying direct URL /new...")
            page.goto("https://share.streamlit.io/new", wait_until="domcontentloaded", timeout=15000)
            time.sleep(5)
            page.wait_for_load_state("networkidle", timeout=15000)
            save_screenshot(page, "streamlit_cloud_new_app_direct.png")

            buttons2 = page.query_selector_all("button")
            for i, btn in enumerate(buttons2):
                try:
                    text = btn.inner_text().strip()
                    if btn.is_visible() and text:
                        print(f"  Button on /new: '{text[:100]}'")
                except Exception:
                    pass

            inputs2 = page.query_selector_all("input, textarea, select")
            for i, inp in enumerate(inputs2):
                try:
                    tag = inp.evaluate("el => el.tagName.toLowerCase()")
                    input_type = inp.get_attribute("type") or ""
                    name = inp.get_attribute("name") or ""
                    placeholder = inp.get_attribute("placeholder") or ""
                    aria_label = inp.get_attribute("aria-label") or ""
                    if inp.is_visible():
                        print(f"  Input on /new: tag={tag} type={input_type} name='{name}' placeholder='{placeholder[:60]}' aria-label='{aria_label[:60]}'")
                except Exception:
                    pass

            body_text = ""
            try:
                body_text = page.inner_text("body")
            except Exception:
                pass
            print(f"  Body text (first 500): {body_text[:500]}")

        if clicked_new_app:
            print("[Step 9] Waiting for app creation form to fully load...")
            time.sleep(8)
            try:
                page.wait_for_load_state("networkidle", timeout=30000)
            except Exception:
                pass
            time.sleep(3)

            print("[Step 9b] Waiting for form inputs to appear...")
            try:
                page.wait_for_selector("input", timeout=20000)
            except Exception:
                pass
            time.sleep(2)

        print("[Step 10] Taking new app form screenshot...")
        save_screenshot(page, "streamlit_cloud_new_app.png")

        print("[Step 10b] Dumping form elements...")
        inputs = page.query_selector_all("input, textarea, select")
        for i, inp in enumerate(inputs):
            try:
                tag = inp.evaluate("el => el.tagName.toLowerCase()")
                input_type = inp.get_attribute("type") or ""
                name = inp.get_attribute("name") or ""
                placeholder = inp.get_attribute("placeholder") or ""
                aria_label = inp.get_attribute("aria-label") or ""
                if inp.is_visible():
                    print(f"  Visible Input[{i}]: tag={tag} type={input_type} name='{name}' placeholder='{placeholder[:60]}' aria-label='{aria_label[:60]}'")
            except Exception:
                pass

        print("[Step 11] Filling in the form...")

        repo_selectors = [
            "input[name='repository']",
            "input[placeholder*='repository' i]",
            "input[placeholder*='repo' i]",
            "input[placeholder*='GitHub' i]",
            "input[name*='repo' i]",
            "input[name*='repository' i]",
            "input[aria-label*='repository' i]",
            "input[aria-label*='repo' i]",
            "input[aria-label*='GitHub' i]",
            "#repository",
            "#repo",
        ]
        repo_input = find_element(page, repo_selectors, timeout=10000)
        if not repo_input:
            print("[Form] Trying first visible text input as repo field...")
            text_inputs = page.query_selector_all("input[type='text'], input:not([type])")
            for inp in text_inputs:
                try:
                    if inp.is_visible():
                        repo_input = inp
                        break
                except Exception:
                    continue

        if repo_input:
            repo_input.click()
            repo_input.fill("")
            time.sleep(0.5)
            repo_input.fill(REPO)
            print(f"[Form] Repository set to: {REPO}")
            time.sleep(1)
        else:
            print("[Form] WARNING: Could not find repository input field")
            save_screenshot(page, "streamlit_cloud_no_repo_field.png")

        branch_selectors = [
            "input[name='branch']",
            "input[placeholder*='branch' i]",
            "input[name*='branch' i]",
            "input[aria-label*='branch' i]",
            "#branch",
            "select[name*='branch' i]",
        ]
        branch_input = find_element(page, branch_selectors, timeout=5000)
        if branch_input:
            tag = branch_input.evaluate("el => el.tagName.toLowerCase()")
            if tag == "select":
                try:
                    branch_input.select_option(value=BRANCH)
                except Exception:
                    branch_input.select_option(label=BRANCH)
            else:
                branch_input.click()
                branch_input.fill("")
                branch_input.fill(BRANCH)
            print(f"[Form] Branch set to: {BRANCH}")
            time.sleep(1)
        else:
            print("[Form] WARNING: Could not find branch input field")

        main_file_selectors = [
            "input[name='mainModule']",
            "input[placeholder*='main file' i]",
            "input[placeholder*='file path' i]",
            "input[placeholder*='filepath' i]",
            "input[placeholder*='main file path' i]",
            "input[placeholder*='entry point' i]",
            "input[placeholder*='app file' i]",
            "input[name*='mainFile' i]",
            "input[name*='main_file' i]",
            "input[name*='filePath' i]",
            "input[name*='file_path' i]",
            "input[aria-label*='main file' i]",
            "input[aria-label*='file path' i]",
            "input[aria-label*='entry point' i]",
            "#mainFilePath",
            "#mainFile",
        ]
        main_file_input = find_element(page, main_file_selectors, timeout=5000)
        if not main_file_input:
            print("[Form] Trying second visible text input as main file field...")
            text_inputs = page.query_selector_all("input[type='text'], input:not([type])")
            input_count = 0
            for inp in text_inputs:
                try:
                    if inp.is_visible():
                        input_count += 1
                        if input_count == 2:
                            main_file_input = inp
                            break
                except Exception:
                    continue
        if main_file_input:
            main_file_input.click()
            main_file_input.fill("")
            main_file_input.fill(MAIN_FILE)
            print(f"[Form] Main file path set to: {MAIN_FILE}")
            time.sleep(1)
        else:
            print("[Form] WARNING: Could not find main file path input field")

        app_name_selectors = [
            "input[placeholder*='app name' i]",
            "input[placeholder*='name' i]",
            "input[name*='appName' i]",
            "input[name*='app_name' i]",
            "input[aria-label*='app name' i]",
            "input[aria-label*='name' i]",
            "#appName",
        ]
        app_name_input = find_element(page, app_name_selectors, timeout=5000)
        if app_name_input:
            app_name_input.click()
            app_name_input.fill("")
            app_name_input.fill(APP_NAME)
            print(f"[Form] App name set to: {APP_NAME}")
            time.sleep(1)
        else:
            print("[Form] WARNING: Could not find app name input field (may be auto-generated)")

        time.sleep(2)
        save_screenshot(page, "streamlit_cloud_form_filled.png")

        print("[Step 12] Clicking 'Deploy' button...")
        deploy_selectors = [
            "button:has-text('Deploy!')",
            "button:has-text('Deploy')",
            "button:has-text('deploy')",
            "input[type='submit'][value*='Deploy' i]",
            "button[type='submit']",
            "[data-testid='deploy-button']",
            "button:has-text('Save')",
            "button:has-text('Launch')",
            "button:has-text('Create')",
            "button:has-text('Submit')",
        ]
        deployed = find_and_click(page, deploy_selectors, timeout=10000)
        if not deployed:
            print("[Step 12b] No 'Deploy' button found. Checking if app already exists...")
            manage_selectors = [
                "button:has-text('Manage app')",
                "a:has-text('Manage app')",
                "button:has-text('Manage')",
                "a:has-text('Manage')",
            ]
            manage_clicked = find_and_click(page, manage_selectors, timeout=5000)
            if manage_clicked:
                print("[Step 12c] Clicked 'Manage app' - app may already exist!")
                time.sleep(5)
                try:
                    page.wait_for_load_state("networkidle", timeout=30000)
                except Exception:
                    pass
                save_screenshot(page, "streamlit_cloud_manage_app.png")
                print(f"  Current URL: {page.url}")

                app_url = page.url
                if ".streamlit.app" in app_url:
                    result["url"] = app_url
                    result["success"] = True
                    print(f"[Success] App already exists! URL: {app_url}")
                else:
                    link_selectors = [
                        "a[href*='.streamlit.app']",
                        "a[href*='wc2026']",
                    ]
                    for sel in link_selectors:
                        try:
                            link = page.query_selector(sel)
                            if link:
                                app_url = link.get_attribute("href")
                                if app_url:
                                    result["url"] = app_url
                                    result["success"] = True
                                    print(f"[Success] App already exists! URL: {app_url}")
                                    break
                        except Exception:
                            continue

                    if not result["url"]:
                        print("[Step 12d] Dumping page elements on manage page...")
                        buttons = page.query_selector_all("button")
                        for i, btn in enumerate(buttons):
                            try:
                                text = btn.inner_text()
                                if btn.is_visible() and text.strip():
                                    print(f"  Button: '{text[:80]}'")
                            except Exception:
                                pass
                        links = page.query_selector_all("a")
                        for i, link in enumerate(links):
                            try:
                                text = link.inner_text().strip()
                                href = link.get_attribute("href") or ""
                                if link.is_visible() and text:
                                    print(f"  Link: '{text[:80]}' href='{href[:100]}'")
                            except Exception:
                                pass
                        save_screenshot(page, "streamlit_cloud_no_deploy_button.png")
                        raise Exception("Could not find 'Deploy' button and could not determine app URL")
            else:
                print("[Step 12b] Dumping all visible buttons for deploy debug...")
                buttons = page.query_selector_all("button")
                for i, btn in enumerate(buttons):
                    try:
                        text = btn.inner_text()
                        if btn.is_visible() and text.strip():
                            print(f"  Visible Button: '{text[:80]}'")
                    except Exception:
                        pass
                save_screenshot(page, "streamlit_cloud_no_deploy_button.png")
                raise Exception("Could not find 'Deploy' button")

        print("[Step 13] Waiting for deployment to start...")
        time.sleep(10)
        page.wait_for_load_state("networkidle", timeout=30000)

        print("[Step 14] Taking deployment screenshot...")
        save_screenshot(page, "streamlit_cloud_deploying.png")

        print("[Step 15] Getting deployed app URL...")
        current_url = page.url
        print(f"[URL] Current page URL: {current_url}")

        app_url = None
        if ".streamlit.app" in current_url:
            app_url = current_url

        if not app_url:
            link_selectors = [
                "a[href*='.streamlit.app']",
                "a[href*='wc2026']",
            ]
            for sel in link_selectors:
                try:
                    link = page.query_selector(sel)
                    if link:
                        app_url = link.get_attribute("href")
                        if app_url:
                            break
                except Exception:
                    continue

        if not app_url:
            time.sleep(15)
            current_url = page.url
            if ".streamlit.app" in current_url:
                app_url = current_url
            save_screenshot(page, "streamlit_cloud_after_wait.png")

        result["url"] = app_url
        result["success"] = app_url is not None

        if app_url:
            print(f"[Success] App URL: {app_url}")
        else:
            print(f"[Info] Could not extract app URL. Current URL: {current_url}")
            result["url"] = current_url

    except Exception as e:
        result["error"] = str(e)
        print(f"[ERROR] {e}")
        try:
            save_screenshot(page, "streamlit_cloud_error.png")
        except Exception:
            pass
    finally:
        print("[Step 16] Closing browser...")
        try:
            context.close()
        except Exception:
            pass

print("\n" + "=" * 60)
print("DEPLOYMENT RESULT")
print("=" * 60)
print(f"Success: {result['success']}")
print(f"URL: {result['url']}")
print(f"Error: {result['error']}")
print("=" * 60)

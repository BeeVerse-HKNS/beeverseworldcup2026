import asyncio
import os
import subprocess
import time
import json
import urllib.request
from playwright.async_api import async_playwright

SCREENSHOT_DIR = r"d:\My_Code_Projects\Harnessing\projects\world-2026-deploy\deploy_screenshots"
DEPLOY_URL = "https://share.streamlit.io/deploy?repository=https://github.com/BeeVerse-HKNS/world-cup-2026-predictor&mainModule=streamlit_app.py&branch=main"
TIMEOUT = 120000
CDP_PORT = 9222
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
TEMP_PROFILE = os.path.join(os.environ.get("TEMP", ""), "streamlit_cdp_profile")


async def screenshot(page, name):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    await page.screenshot(path=path, full_page=True)
    print(f"[Screenshot] {name} -> {path}")


def wait_for_cdp(port, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            url = f"http://localhost:{port}/json/version"
            req = urllib.request.urlopen(url, timeout=2)
            data = json.loads(req.read())
            print(f"[CDP] Connected: {data.get('Browser', 'unknown')}")
            return True
        except Exception:
            time.sleep(1)
    return False


async def wait_for_login(page, max_wait=600):
    print("=" * 60)
    print("[ACTION REQUIRED] Please log in to Streamlit Cloud!")
    print("  1. In the Chrome window, complete the login flow")
    print("  2. Use jonathan.kwan@beeverse.io to log in")
    print("  3. The script will auto-detect when login is complete")
    print("=" * 60)
    for i in range(max_wait // 5):
        await asyncio.sleep(5)
        current_url = page.url
        page_text = ""
        try:
            page_text = await page.inner_text("body")
        except Exception:
            pass

        is_login_url = (
            "authkit.streamlit.io" in current_url
            or "login.streamlit.io" in current_url
            or "accounts.google.com" in current_url
            or "github.com/login" in current_url
            or "email-verification" in current_url
        )

        has_deploy_form = (
            "deploy an app" in page_text.lower()
            or 'name="repository"' in (await page.content()).lower()
            or 'data-testid="deploy-button"' in (await page.content()).lower()
        )

        has_sign_in_button = "continue to sign-in" in page_text.lower()

        if has_deploy_form:
            print(f"\n[Login] Completed! Deploy form detected. URL: {current_url}")
            return True

        if not is_login_url and not has_sign_in_button:
            print(f"\n[Login] URL changed away from login pages. URL: {current_url}")
            print(f"[Login] Page text snippet: {page_text[:200]}")
            await asyncio.sleep(3)
            try:
                page_text2 = await page.inner_text("body")
                if "deploy an app" in page_text2.lower() or "continue to sign-in" not in page_text2.lower():
                    print(f"[Login] Confirmed login complete!")
                    return True
            except Exception:
                pass

        if i % 6 == 0:
            print(f"  Waiting for login... {i*5}s elapsed (URL: {current_url[:60]}...)")
    return False


async def main():
    print("[Step 0] Closing existing Chrome instances...")
    subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
    await asyncio.sleep(3)

    if os.path.exists(TEMP_PROFILE):
        import shutil
        shutil.rmtree(TEMP_PROFILE, ignore_errors=True)

    print(f"[Step 0] Launching Chrome with CDP on port {CDP_PORT}...")
    chrome_proc = subprocess.Popen([
        CHROME_PATH,
        f"--remote-debugging-port={CDP_PORT}",
        f"--user-data-dir={TEMP_PROFILE}",
        "--no-first-run",
        "--no-default-browser-check",
        "--window-size=1440,900",
    ])
    await asyncio.sleep(3)

    if not wait_for_cdp(CDP_PORT):
        print("[ERROR] Chrome CDP not ready after 30s. Aborting.")
        return None

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f"http://localhost:{CDP_PORT}")
        print(f"[Step 0] Connected! Contexts: {len(browser.contexts)}")

        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = context.pages[0] if context.pages else await context.new_page()

        print("[Step 1] Navigating to Streamlit Cloud deploy URL...")
        await page.goto(DEPLOY_URL, wait_until="domcontentloaded", timeout=TIMEOUT)
        await asyncio.sleep(5)
        await screenshot(page, "01_initial_page")

        page_text = ""
        try:
            page_text = await page.inner_text("body")
        except Exception:
            pass

        needs_login = (
            "authkit.streamlit.io" in page.url
            or "login.streamlit.io" in page.url
            or "accounts.google.com" in page.url
            or "github.com/login" in page.url
            or "continue to sign-in" in page_text.lower()
            or ("sign in" in page_text.lower() and "deploy an app" not in page_text.lower())
        )

        if needs_login:
            await wait_for_login(page)
            await asyncio.sleep(3)
            current_url = page.url
            if "deploy" not in current_url:
                print("[Step 1b] Navigating back to deploy URL after login...")
                await page.goto(DEPLOY_URL, wait_until="domcontentloaded", timeout=TIMEOUT)
                await asyncio.sleep(5)
            await screenshot(page, "01b_after_login")

        print("[Step 2] Checking deploy form...")
        await asyncio.sleep(3)
        await screenshot(page, "02_deploy_form")

        page_text = ""
        try:
            page_text = await page.inner_text("body")
        except Exception:
            pass
        print(f"[Step 2] Page URL: {page.url}")
        print(f"[Step 2] Page text (first 800 chars): {page_text[:800]}")

        if "deploy an app" not in page_text.lower() and "deploy" not in page_text.lower():
            print("[Step 2] Deploy form not found. Checking if still on login page...")
            needs_login_v2 = (
                "sign in" in page_text.lower()
                or "authkit" in page.url
                or "login" in page.url
            )
            if needs_login_v2:
                await wait_for_login(page)
                await asyncio.sleep(3)
                if "deploy" not in page.url:
                    await page.goto(DEPLOY_URL, wait_until="domcontentloaded", timeout=TIMEOUT)
                    await asyncio.sleep(5)
                await screenshot(page, "02b_after_second_login")

        repo_input = page.locator('input[name="repository"]')
        branch_input = page.locator('input[name="branch"]')
        module_input = page.locator('input[name="mainModule"]')

        if await repo_input.count() > 0:
            repo_val = await repo_input.first.input_value()
            print(f"  Repository: '{repo_val}'")
            if "https://github.com/" in repo_val:
                print("[Step 2a] Repository has full URL format. Clearing and using owner/repo format...")
                await repo_input.first.click()
                await asyncio.sleep(0.3)
                await repo_input.first.fill("")
                await asyncio.sleep(0.3)
                await repo_input.first.fill("BeeVerse-HKNS/world-cup-2026-predictor")
                await asyncio.sleep(3)
                new_val = await repo_input.first.input_value()
                print(f"  New repository value: '{new_val}'")

        if await branch_input.count() > 0:
            branch_val = await branch_input.first.input_value()
            print(f"  Branch: '{branch_val}'")
            if not branch_val:
                await branch_input.first.fill("main")
                await asyncio.sleep(1)

        if await module_input.count() > 0:
            module_val = await module_input.first.input_value()
            print(f"  Main file: '{module_val}'")
            if not module_val:
                await module_input.first.fill("streamlit_app.py")
                await asyncio.sleep(1)

        await asyncio.sleep(3)
        await screenshot(page, "03_form_filled")

        page_text = ""
        try:
            page_text = await page.inner_text("body")
        except Exception:
            pass
        print(f"[Step 3] Page text after filling: {page_text[:500]}")

        deploy_btn = page.locator('button[data-testid="deploy-button"], button:has-text("Deploy")')
        btn_count = await deploy_btn.count()
        print(f"[Step 3] Deploy buttons found: {btn_count}")

        if btn_count > 0:
            is_disabled = await deploy_btn.first.is_disabled()
            print(f"  Deploy button disabled: {is_disabled}")

            if is_disabled:
                print("[Step 3a] Button is disabled. Checking error messages...")
                error_texts = page.locator('[class*="error"], [class*="warning"], [role="alert"], [color*="red"]')
                err_count = await error_texts.count()
                for i in range(min(err_count, 10)):
                    try:
                        txt = await error_texts.nth(i).inner_text()
                        if txt.strip():
                            print(f"  Error {i}: '{txt.strip()}'")
                    except Exception:
                        pass

                print("[Step 3a] Trying to remove disabled attribute via JS...")
                try:
                    await page.evaluate("""
                        const btn = document.querySelector('button[data-testid="deploy-button"]');
                        if (btn) {
                            btn.removeAttribute('disabled');
                            btn.classList.remove('disabled');
                        }
                    """)
                    await asyncio.sleep(1)
                    is_disabled = await deploy_btn.first.is_disabled()
                    print(f"  Deploy button disabled after JS fix: {is_disabled}")
                except Exception as e:
                    print(f"  JS fix failed: {e}")

            try:
                await deploy_btn.first.click(timeout=10000)
                print("[Step 3] Clicked Deploy button!")
            except Exception as e:
                print(f"[Step 3] Normal click failed: {e}")
                print("[Step 3] Trying force click...")
                try:
                    await deploy_btn.first.click(force=True, timeout=10000)
                    print("[Step 3] Force clicked Deploy button!")
                except Exception as e2:
                    print(f"[Step 3] Force click also failed: {e2}")
                    print("[Step 3] Trying JS click...")
                    try:
                        await page.evaluate("""
                            const btn = document.querySelector('button[data-testid="deploy-button"]');
                            if (btn) btn.click();
                        """)
                        print("[Step 3] JS click executed!")
                    except Exception as e3:
                        print(f"[Step 3] JS click also failed: {e3}")
        else:
            print("[Step 3] No Deploy button found!")
            all_buttons = page.locator("button")
            total = await all_buttons.count()
            for i in range(min(total, 20)):
                try:
                    txt = await all_buttons.nth(i).inner_text()
                    disabled = await all_buttons.nth(i).is_disabled()
                    if txt.strip():
                        print(f"  Button {i}: '{txt.strip()}' (disabled={disabled})")
                except Exception:
                    pass

        await asyncio.sleep(3)
        await screenshot(page, "04_after_deploy_click")

        print("[Step 4] Waiting for deployment to start/complete...")
        deployed_url = None
        start_time = time.time()

        while time.time() - start_time < 180:
            await asyncio.sleep(5)
            elapsed = int(time.time() - start_time)
            print(f"  Waiting... {elapsed}s elapsed")

            current_url = page.url
            print(f"  Current URL: {current_url}")

            if "streamlit.app" in current_url and "share.streamlit.io" not in current_url:
                deployed_url = current_url
                print(f"[Step 4] Deployment URL detected: {deployed_url}")
                break

            url_elements = page.locator('a[href*="streamlit.app"]')
            if await url_elements.count() > 0:
                href = await url_elements.first.get_attribute("href")
                if href and "streamlit.app" in href:
                    deployed_url = href
                    print(f"[Step 4] Found deployed URL link: {deployed_url}")
                    break

            page_text = ""
            try:
                page_text = await page.inner_text("body")
            except Exception:
                pass

            success_keywords = ["your app is live", "app is live", "successfully deployed", "world-cup-2026-predictor.streamlit.app"]
            for kw in success_keywords:
                if kw.lower() in page_text.lower():
                    print(f"[Step 4] Success keyword found: '{kw}'")

            if elapsed % 15 == 0 and elapsed > 0:
                await screenshot(page, f"05_deploy_progress_{elapsed}s")

        await screenshot(page, "06_final_state")

        if not deployed_url:
            print("[Step 5] Checking page for any URL clues...")
            try:
                page_text = await page.inner_text("body")
                for line in page_text.split("\n"):
                    if "streamlit.app" in line.lower():
                        print(f"  Found URL in page text: {line.strip()}")
                        deployed_url = line.strip()
                        break
            except Exception:
                pass

            if not deployed_url:
                current_url = page.url
                if "streamlit.app" in current_url:
                    deployed_url = current_url

        if deployed_url:
            deployed_url = deployed_url.split("?")[0].rstrip("/")
            print(f"\n{'='*60}")
            print(f"DEPLOYED URL: {deployed_url}")
            print(f"{'='*60}")
        else:
            print("\n[WARNING] Could not automatically detect deployed URL.")
            print("Check the screenshots for the current state.")
            print(f"Final page URL: {page.url}")

        await asyncio.sleep(3)
        browser.close()

        return deployed_url


if __name__ == "__main__":
    result = asyncio.run(main())
    if result:
        print(f"\nFINAL_RESULT: {result}")

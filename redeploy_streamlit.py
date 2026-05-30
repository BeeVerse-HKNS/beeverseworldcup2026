import asyncio
import os
import sys
import time
from playwright.async_api import async_playwright

SCREENSHOT_DIR = r"d:\My_Code_Projects\Harnessing\projects\world-2026-deploy\deploy_screenshots"
PROFILE_DIR = r"d:\My_Code_Projects\Harnessing\projects\world-2026-deploy\browser_profile"
REPO = "BeeVerse-HKNS/world-cup-2026-predictor"
BRANCH = "main"
MAIN_FILE = "streamlit_app.py"
EXPECTED_URL = "https://beeverseworldcup2026.streamlit.app"
CDP_URL = "http://localhost:9222"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(PROFILE_DIR, exist_ok=True)


async def screenshot(page, name):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    try:
        await page.screenshot(path=path, full_page=True)
        print(f"[Screenshot] {name}", flush=True)
    except Exception as e:
        print(f"[Screenshot] Failed {name}: {e}", flush=True)
    return path


async def is_logged_in(page):
    try:
        url = page.url.lower()
        if any(x in url for x in ["github.com/login", "authkit.streamlit", "accounts.streamlit"]):
            return False
        body = await page.evaluate("() => document.body.innerText.substring(0, 1000)")
        if "Continue to sign-in" in body or "Sign in" in body[:200]:
            return False
        return True
    except Exception:
        return False


async def main():
    print("=" * 60, flush=True)
    print("Streamlit Cloud Redeploy Script v3", flush=True)
    print(f"Repo: {REPO} | Branch: {BRANCH} | File: {MAIN_FILE}", flush=True)
    print(f"Profile: {PROFILE_DIR}", flush=True)
    print("=" * 60, flush=True)

    async with async_playwright() as p:
        browser = None
        is_cdp = False

        try:
            browser = await p.chromium.connect_over_cdp(CDP_URL)
            is_cdp = True
            print(f"[CDP] Connected to existing Chrome on {CDP_URL}", flush=True)
        except Exception:
            pass

        if not browser:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=PROFILE_DIR,
                headless=False,
                args=["--start-maximized", "--disable-blink-features=AutomationControlled"],
                viewport={"width": 1920, "height": 1080},
                no_viewport=False,
            )
            browser = context
            print("[Browser] Launched Chromium with persistent profile", flush=True)

        if is_cdp:
            contexts = browser.contexts
            page = await contexts[0].new_page() if contexts else await browser.new_page()
        else:
            if len(context.pages) > 0:
                page = context.pages[0]
            else:
                page = await context.new_page()

        print("\n[Step 1] Navigating to Streamlit Cloud...", flush=True)
        await page.goto("https://share.streamlit.io/", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(5)
        await screenshot(page, "v3_01_initial")

        logged_in = await is_logged_in(page)
        print(f"  Logged in: {logged_in} | URL: {page.url[:80]}", flush=True)

        if not logged_in:
            print("\n" + "!" * 60, flush=True)
            print("  LOGIN REQUIRED!", flush=True)
            print("  A browser window has opened.", flush=True)
            print("  Please complete the GitHub login in that window.", flush=True)
            print("  Email: jonathan.kwan@beeverse.io", flush=True)
            print("  The script will wait up to 5 minutes...", flush=True)
            print("!" * 60, flush=True)
            await screenshot(page, "v3_02_login_page")

            github_logged_in = False
            for i in range(150):
                await asyncio.sleep(2)
                try:
                    cur = page.url
                except Exception:
                    continue

                if "github.com/session" in cur or ("github.com" in cur and "/login" not in cur):
                    github_logged_in = True
                    print(f"  GitHub login detected! Navigating back to Streamlit Cloud...", flush=True)
                    await asyncio.sleep(2)
                    await page.goto("https://share.streamlit.io/", wait_until="networkidle", timeout=30000)
                    await asyncio.sleep(5)
                    break

                if i % 15 == 0 and i > 0:
                    print(f"  Still waiting for login... ({i*2}s) URL: {cur[:80]}", flush=True)
                    await screenshot(page, f"v3_02c_wait_{i*2}s")

            if github_logged_in:
                logged_in = await is_logged_in(page)
                if not logged_in:
                    print("  GitHub logged in but Streamlit session not established. Retrying login flow...", flush=True)
                    try:
                        continue_btn = await page.query_selector('button:has-text("Continue to sign-in")')
                        if continue_btn:
                            await continue_btn.click()
                            await asyncio.sleep(10)
                    except Exception:
                        pass

                    for i in range(30):
                        await asyncio.sleep(2)
                        logged_in = await is_logged_in(page)
                        if logged_in:
                            print(f"  Streamlit login confirmed! URL: {page.url[:80]}", flush=True)
                            break
                        print(f"  Waiting for Streamlit session... ({i*2}s)", flush=True)

            if not logged_in:
                logged_in = await is_logged_in(page)

            if not logged_in:
                print("  Login timeout after 5 minutes!", flush=True)
                await screenshot(page, "v3_02d_timeout")
                print(f"\n{'=' * 60}", flush=True)
                print("RESULT: Login required but not completed", flush=True)
                print(f"Error: User login timeout", flush=True)
                print(f"Tip: Re-run the script - the persistent profile will remember your login", flush=True)
                print(f"{'=' * 60}", flush=True)
                if not is_cdp:
                    await context.close()
                return

        await asyncio.sleep(3)
        await screenshot(page, "v3_03_after_login")

        print("\n[Step 2] Inspecting dashboard...", flush=True)
        body_text = ""
        try:
            body_text = await page.evaluate("() => document.body.innerText.substring(0, 3000)")
        except Exception:
            pass
        print(f"  Page text: {body_text[:500]}", flush=True)

        all_links = await page.query_selector_all("a")
        print(f"  Found {len(all_links)} links", flush=True)
        for link in all_links:
            try:
                text = (await link.text_content() or "").strip()
                href = await link.get_attribute("href") or ""
                if text or href:
                    print(f"    Link: '{text[:60]}' -> '{href[:80]}'", flush=True)
            except Exception:
                continue

        all_buttons = await page.query_selector_all("button")
        print(f"  Found {len(all_buttons)} buttons", flush=True)
        for btn in all_buttons:
            try:
                text = (await btn.text_content() or "").strip()
                visible = await btn.is_visible()
                if visible and text:
                    print(f"    Button: '{text[:60]}' (visible)", flush=True)
            except Exception:
                continue

        print("\n[Step 3] Looking for existing app or deploy option...", flush=True)
        app_found = False
        for link in all_links:
            try:
                text = (await link.text_content() or "").strip().lower()
                href = (await link.get_attribute("href") or "").lower()
                if ("world-cup" in text or "predictor" in text) and "streamlit.app" in href:
                    print(f"  Found app link: '{text}' -> '{href}'", flush=True)
                    await link.click()
                    await asyncio.sleep(5)
                    await screenshot(page, "v3_04_app_detail")
                    app_found = True
                    break
            except Exception:
                continue

        if not app_found:
            for link in all_links:
                try:
                    href = (await link.get_attribute("href") or "").lower()
                    if "beeverseworldcup2026.streamlit.app" in href:
                        print(f"  Found app by URL: '{href}'", flush=True)
                        await link.click()
                        await asyncio.sleep(5)
                        await screenshot(page, "v3_04_app_detail")
                        app_found = True
                        break
                except Exception:
                    continue

        if app_found:
            print("  Found existing app, looking for Reboot/Settings...", flush=True)
            for sel in ['button:has-text("Reboot")', 'a:has-text("Settings")', 'button:has-text("Settings")']:
                try:
                    btn = await page.query_selector(sel)
                    if btn:
                        text = (await btn.text_content() or "").strip()
                        print(f"  Clicking: {text}", flush=True)
                        await btn.click()
                        await asyncio.sleep(3)
                        await screenshot(page, "v3_05_settings")
                        break
                except Exception:
                    continue

            for sel in ['button:has-text("Reboot app")', 'button:has-text("Redeploy")']:
                try:
                    btn = await page.query_selector(sel)
                    if btn:
                        await btn.click()
                        await asyncio.sleep(2)
                        confirm = await page.query_selector('button:has-text("Yes"), button:has-text("Confirm")')
                        if confirm:
                            await confirm.click()
                        await asyncio.sleep(5)
                        await screenshot(page, "v3_06_reboot")
                        break
                except Exception:
                    continue

        print("\n[Step 4] Navigating to deploy page...", flush=True)
        await page.goto("https://share.streamlit.io/", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)
        await screenshot(page, "v3_07_dashboard")

        new_app_found = False
        for sel in ['a:has-text("New app")', 'button:has-text("New app")', 'a:has-text("Create app")', 'button:has-text("Create app")', 'a[href*="/new"]']:
            try:
                btn = await page.query_selector(sel)
                if btn:
                    visible = await btn.is_visible()
                    if visible:
                        text = (await btn.text_content() or "").strip()
                        print(f"  Found deploy button: '{text}'", flush=True)
                        await btn.click()
                        await asyncio.sleep(5)
                        await screenshot(page, "v3_08_deploy_form")
                        new_app_found = True
                        break
            except Exception:
                continue

        if not new_app_found:
            print("  No 'New app' button found, trying direct deploy URL...", flush=True)
            deploy_url = f"https://share.streamlit.io/deploy?repository={REPO.replace('/', '%2F')}&branch={BRANCH}&mainFile={MAIN_FILE}"
            await page.goto(deploy_url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(5)
            await screenshot(page, "v3_08b_direct_deploy")

        print("\n[Step 5] Checking for 'Deploy now' option...", flush=True)
        deploy_now = await page.query_selector('a:has-text("Deploy now"), button:has-text("Deploy now")')
        if deploy_now:
            print("  Found 'Deploy now' option, clicking...", flush=True)
            await deploy_now.click()
            await asyncio.sleep(5)
            await screenshot(page, "v3_08c_deploy_now")
        else:
            print("  No 'Deploy now' option found, continuing with current page...", flush=True)

        print("\n[Step 5b] Inspecting deploy form...", flush=True)
        await asyncio.sleep(3)

        all_inputs = await page.query_selector_all("input")
        print(f"  Found {len(all_inputs)} inputs", flush=True)
        for i, inp in enumerate(all_inputs):
            try:
                itype = await inp.get_attribute("type") or ""
                name = await inp.get_attribute("name") or ""
                placeholder = await inp.get_attribute("placeholder") or ""
                value = await inp.get_attribute("value") or ""
                aria = await inp.get_attribute("aria-label") or ""
                visible = await inp.is_visible()
                if visible:
                    print(f"    Input[{i}]: type='{itype}' name='{name}' placeholder='{placeholder}' value='{value}' aria='{aria}'", flush=True)
            except Exception:
                continue

        all_buttons2 = await page.query_selector_all("button")
        for btn in all_buttons2:
            try:
                text = (await btn.text_content() or "").strip()
                visible = await btn.is_visible()
                if visible and text:
                    print(f"    Button: '{text[:80]}'", flush=True)
            except Exception:
                continue

        try:
            body_text2 = await page.evaluate("() => document.body.innerText.substring(0, 3000)")
            print(f"\n  Page text:\n{body_text2[:2000]}", flush=True)
        except Exception:
            pass

        print("\n[Step 6] Filling deploy form...", flush=True)
        repo_filled = False
        for inp in all_inputs:
            try:
                visible = await inp.is_visible()
                if not visible:
                    continue
                placeholder = (await inp.get_attribute("placeholder") or "").lower()
                name = (await inp.get_attribute("name") or "").lower()
                aria = (await inp.get_attribute("aria-label") or "").lower()
                value = (await inp.get_attribute("value") or "")
                if any(kw in placeholder or kw in name or kw in aria for kw in ["repo", "repository", "owner"]):
                    await inp.click()
                    await inp.fill("")
                    await inp.type(REPO, delay=30)
                    repo_filled = True
                    print(f"  Filled repository", flush=True)
                    break
            except Exception:
                continue

        if not repo_filled:
            for inp in all_inputs:
                try:
                    visible = await inp.is_visible()
                    itype = await inp.get_attribute("type") or ""
                    if visible and itype in ["text", ""]:
                        await inp.click()
                        await inp.fill("")
                        await inp.type(REPO, delay=30)
                        repo_filled = True
                        print(f"  Filled first visible text input with repo", flush=True)
                        break
                except Exception:
                    continue

        await asyncio.sleep(1)

        for inp in all_inputs:
            try:
                visible = await inp.is_visible()
                if not visible:
                    continue
                placeholder = (await inp.get_attribute("placeholder") or "").lower()
                name = (await inp.get_attribute("name") or "").lower()
                aria = (await inp.get_attribute("aria-label") or "").lower()
                if "branch" in placeholder or "branch" in name or "branch" in aria:
                    await inp.click()
                    await inp.fill("")
                    await inp.type(BRANCH, delay=30)
                    print(f"  Filled branch", flush=True)
                    break
            except Exception:
                continue

        await asyncio.sleep(1)

        for inp in all_inputs:
            try:
                visible = await inp.is_visible()
                if not visible:
                    continue
                placeholder = (await inp.get_attribute("placeholder") or "").lower()
                name = (await inp.get_attribute("name") or "").lower()
                aria = (await inp.get_attribute("aria-label") or "").lower()
                if any(kw in placeholder or kw in name or kw in aria for kw in ["main file", "file path", "mainfile", "entry point"]):
                    await inp.click()
                    await inp.fill("")
                    await inp.type(MAIN_FILE, delay=30)
                    print(f"  Filled main file", flush=True)
                    break
            except Exception:
                continue

        await asyncio.sleep(2)
        await screenshot(page, "v3_09_form_filled")

        print("\n[Step 7] Clicking Deploy button...", flush=True)
        deploy_clicked = False
        for sel in ['button:has-text("Deploy!")', 'button:has-text("Deploy")', 'button[type="submit"]']:
            try:
                btn = await page.query_selector(sel)
                if btn:
                    visible = await btn.is_visible()
                    if visible:
                        text = (await btn.text_content() or "").strip()
                        print(f"  Clicking: '{text}'", flush=True)
                        await btn.click()
                        deploy_clicked = True
                        break
            except Exception:
                continue

        if not deploy_clicked:
            for btn in all_buttons2:
                try:
                    text = (await btn.text_content() or "").strip().lower()
                    visible = await btn.is_visible()
                    if visible and "deploy" in text:
                        print(f"  Clicking (broad): '{text}'", flush=True)
                        await btn.click()
                        deploy_clicked = True
                        break
                except Exception:
                    continue

        if not deploy_clicked:
            print("  Deploy button NOT found!", flush=True)
            await screenshot(page, "v3_10_no_deploy")
            print(f"\n{'=' * 60}", flush=True)
            print("RESULT: Could not find deploy button", flush=True)
            print(f"Deployed URL: N/A", flush=True)
            print(f"Error: Deploy button not found", flush=True)
            print(f"Screenshots: {SCREENSHOT_DIR}", flush=True)
            print(f"{'=' * 60}", flush=True)
            if not is_cdp:
                await context.close()
            return

        await asyncio.sleep(5)
        await screenshot(page, "v3_11_after_deploy")

        print("\n[Step 8] Waiting for deployment (up to 180s)...", flush=True)
        start = time.time()
        last_ss = 0
        deploy_success = False
        deploy_result = "Timeout"

        while time.time() - start < 180:
            elapsed = int(time.time() - start)

            if elapsed - last_ss >= 20:
                await screenshot(page, f"v3_12_progress_{elapsed}s")
                last_ss = elapsed

            try:
                cur = page.url
                if "beeverseworldcup2026" in cur and "deploy" not in cur.lower() and "share" not in cur.lower():
                    deploy_success = True
                    deploy_result = cur
                    print(f"  Deployed! URL: {cur}", flush=True)
                    break
            except Exception:
                pass

            try:
                errors = await page.query_selector_all('[class*="error"], [class*="Error"], [role="alert"]')
                for el in errors:
                    text = (await el.text_content() or "").strip()
                    if text and len(text) > 5:
                        print(f"  [ERROR] {text[:200]}", flush=True)
                        await screenshot(page, f"v3_13_error_{elapsed}s")
                        deploy_result = f"Error: {text[:500]}"
            except Exception:
                pass

            try:
                body = await page.evaluate("() => document.body.innerText.substring(0, 500)")
                if "Your app is live" in body or "App is live" in body:
                    deploy_success = True
                    deploy_result = "App is live"
                    break
            except Exception:
                pass

            await asyncio.sleep(3)

        await screenshot(page, "v3_14_final")

        print("\n[Step 9] Verifying app...", flush=True)
        try:
            await page.goto(EXPECTED_URL, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(8)
            await screenshot(page, "v3_15_verify")

            verify_errors = []
            error_els = await page.query_selector_all('[class*="error"], [class*="Error"], [class*="exception"], pre, [class*="traceback"]')
            for el in error_els:
                text = (await el.text_content() or "").strip()
                if text and len(text) > 10:
                    verify_errors.append(text.strip()[:300])

            verify_ok = len(verify_errors) == 0
            verify_msg = "\n".join(verify_errors[:3]) if verify_errors else "App loaded without visible errors"
        except Exception as e:
            verify_ok = False
            verify_msg = str(e)

        print(f"\n{'=' * 60}", flush=True)
        print("FINAL RESULT", flush=True)
        print(f"Deployed URL: {EXPECTED_URL}", flush=True)
        print(f"Deploy Success: {deploy_success}", flush=True)
        print(f"Deploy Result: {deploy_result}", flush=True)
        print(f"App Verify: {'OK' if verify_ok else 'ERROR'}", flush=True)
        print(f"Verify Detail: {verify_msg[:500]}", flush=True)
        print(f"Screenshots: {SCREENSHOT_DIR}", flush=True)
        print(f"{'=' * 60}", flush=True)

        if not is_cdp:
            await context.close()


if __name__ == "__main__":
    asyncio.run(main())

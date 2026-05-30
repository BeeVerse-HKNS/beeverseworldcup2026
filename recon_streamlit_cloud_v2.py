import os
import time
import json
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = r"d:\My_Code_Projects\Harnessing\projects\world-2026\deploy_screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def save_screenshot(page, filename):
    path = os.path.join(SCREENSHOT_DIR, filename)
    page.screenshot(path=path, full_page=True)
    print(f"[Screenshot] Saved: {path}")
    return path


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()

    try:
        print("[1] Navigating to https://share.streamlit.io/ ...")
        page.goto("https://share.streamlit.io/", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(3)

        print("[2] Clicking 'Continue to sign-in'...")
        try:
            btn = page.wait_for_selector("button:has-text('Continue to sign-in')", timeout=10000)
            if btn:
                btn.click()
                print("  Clicked 'Continue to sign-in'")
                time.sleep(3)
        except Exception:
            print("  No 'Continue to sign-in' button found, might already be logged in")

        print(f"[3] Current URL: {page.url}")
        save_screenshot(page, "recon2_after_signin_click.png")

        print("=" * 60)
        print("NOT LOGGED IN - Please log in with your GitHub account")
        print("(BeeVerse-HKNS) in the browser window")
        print("=" * 60)

        print("[4] Waiting up to 180s for login...")
        login_wait_start = time.time()
        login_success = False
        while time.time() - login_wait_start < 180:
            time.sleep(5)
            current_url = page.url
            body_text = ""
            try:
                body_text = page.inner_text("body")
            except Exception:
                pass

            has_login_btn = False
            try:
                el = page.query_selector("button:has-text('Continue to sign-in')")
                if el and el.is_visible():
                    has_login_btn = True
            except Exception:
                pass

            if not has_login_btn and "share.streamlit.io" in current_url:
                login_success = True
                print("[Login] Successfully logged in!")
                break

            elapsed = int(time.time() - login_wait_start)
            print(f"[Login] Still waiting... URL={current_url[:60]} ({elapsed}s / 180s)")

        if not login_success:
            save_screenshot(page, "recon2_login_timeout.png")
            raise Exception("Login timeout")

        time.sleep(5)
        page.wait_for_load_state("networkidle", timeout=30000)
        save_screenshot(page, "recon2_logged_in.png")
        print(f"[5] Logged in URL: {page.url}")

        print("[6] Dumping ALL interactive elements on the page...")
        all_buttons = page.query_selector_all("button")
        print(f"  Total buttons: {len(all_buttons)}")
        for i, btn in enumerate(all_buttons):
            try:
                text = btn.inner_text().strip()
                href = btn.get_attribute("href") or ""
                classes = btn.get_attribute("class") or ""
                visible = btn.is_visible()
                onclick = btn.get_attribute("onclick") or ""
                if visible:
                    print(f"  Button[{i}]: text='{text[:100]}' class='{classes[:60]}'")
            except Exception as e:
                print(f"  Button[{i}]: error - {e}")

        all_links = page.query_selector_all("a")
        print(f"\n  Total links: {len(all_links)}")
        for i, link in enumerate(all_links):
            try:
                text = link.inner_text().strip()
                href = link.get_attribute("href") or ""
                visible = link.is_visible()
                if visible and (text or href):
                    print(f"  Link[{i}]: text='{text[:80]}' href='{href[:100]}'")
            except Exception:
                pass

        all_inputs = page.query_selector_all("input, textarea, select")
        print(f"\n  Total inputs: {len(all_inputs)}")
        for i, inp in enumerate(all_inputs):
            try:
                tag = inp.evaluate("el => el.tagName.toLowerCase()")
                input_type = inp.get_attribute("type") or ""
                name = inp.get_attribute("name") or ""
                placeholder = inp.get_attribute("placeholder") or ""
                aria_label = inp.get_attribute("aria-label") or ""
                visible = inp.is_visible()
                if visible:
                    print(f"  Input[{i}]: tag={tag} type={input_type} name='{name}' placeholder='{placeholder[:60]}' aria-label='{aria_label[:60]}'")
            except Exception:
                pass

        print("[7] Dumping page body text (first 2000 chars)...")
        body_text = page.inner_text("body")
        print(body_text[:2000])

        print("[8] Trying to find workspace/dashboard URL patterns...")
        for url_path in ["/workspace", "/dashboard", "/apps", "/new", "/create"]:
            print(f"  Trying {url_path}...")
            page.goto(f"https://share.streamlit.io{url_path}", wait_until="domcontentloaded", timeout=15000)
            time.sleep(3)
            page.wait_for_load_state("networkidle", timeout=15000)
            actual_url = page.url
            print(f"    Redirected to: {actual_url}")
            save_screenshot(page, f"recon2_path_{url_path.replace('/', '_')}.png")

            buttons_on_page = page.query_selector_all("button")
            for i, btn in enumerate(buttons_on_page):
                try:
                    text = btn.inner_text().strip()
                    if btn.is_visible() and text:
                        print(f"    Button: '{text[:80]}'")
                except Exception:
                    pass

            links_on_page = page.query_selector_all("a")
            for i, link in enumerate(links_on_page):
                try:
                    text = link.inner_text().strip()
                    href = link.get_attribute("href") or ""
                    if link.is_visible() and text:
                        print(f"    Link: '{text[:80]}' href='{href[:80]}'")
                except Exception:
                    pass

        print("[9] Final screenshot...")
        save_screenshot(page, "recon2_final.png")

    except Exception as e:
        print(f"[ERROR] {e}")
        try:
            save_screenshot(page, "recon2_error.png")
        except Exception:
            pass
    finally:
        print("[Done] Closing browser...")
        browser.close()

print("Reconnaissance 2 complete!")

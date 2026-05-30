import os
import time
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
        save_screenshot(page, "recon_landing.png")

        print("[2] Checking current URL:", page.url)

        print("[3] Dumping page HTML structure (first 5000 chars)...")
        html = page.content()
        with open(os.path.join(SCREENSHOT_DIR, "recon_page_source.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[HTML] Page source saved ({len(html)} chars)")

        print("[4] Looking for all buttons...")
        buttons = page.query_selector_all("button")
        for i, btn in enumerate(buttons):
            try:
                text = btn.inner_text()
                href = btn.get_attribute("href") or ""
                classes = btn.get_attribute("class") or ""
                visible = btn.is_visible()
                print(f"  Button[{i}]: text='{text[:80]}' href='{href[:50]}' class='{classes[:50]}' visible={visible}")
            except Exception as e:
                print(f"  Button[{i}]: error - {e}")

        print("[5] Looking for all links...")
        links = page.query_selector_all("a")
        for i, link in enumerate(links):
            try:
                text = link.inner_text()
                href = link.get_attribute("href") or ""
                visible = link.is_visible()
                if visible and text.strip():
                    print(f"  Link[{i}]: text='{text[:80]}' href='{href[:80]}' visible={visible}")
            except Exception:
                pass

        print("[6] Looking for all input fields...")
        inputs = page.query_selector_all("input, textarea, select")
        for i, inp in enumerate(inputs):
            try:
                tag = inp.evaluate("el => el.tagName.toLowerCase()")
                input_type = inp.get_attribute("type") or ""
                name = inp.get_attribute("name") or ""
                placeholder = inp.get_attribute("placeholder") or ""
                aria_label = inp.get_attribute("aria-label") or ""
                visible = inp.is_visible()
                print(f"  Input[{i}]: tag={tag} type={input_type} name='{name}' placeholder='{placeholder[:50]}' aria-label='{aria_label[:50]}' visible={visible}")
            except Exception as e:
                print(f"  Input[{i}]: error - {e}")

        print("[7] Looking for iframes...")
        iframes = page.frames
        for i, frame in enumerate(iframes):
            print(f"  Frame[{i}]: url={frame.url[:100]} name={frame.name}")

        print("[8] Checking for 'New app' or 'Create' text anywhere...")
        body_text = page.inner_text("body")
        for keyword in ["New app", "Create", "Deploy", "Sign in", "Log in", "Workspace", "My apps", "App"]:
            if keyword.lower() in body_text.lower():
                idx = body_text.lower().index(keyword.lower())
                context_snippet = body_text[max(0, idx - 30):idx + 50]
                print(f"  Found '{keyword}' in body: ...{context_snippet}...")

        print("[9] Taking full page screenshot...")
        save_screenshot(page, "recon_full_page.png")

        print("[10] Trying to navigate directly to deploy page...")
        page.goto("https://share.streamlit.io/deploy", wait_until="domcontentloaded", timeout=15000)
        time.sleep(3)
        save_screenshot(page, "recon_deploy_page.png")
        print("  Deploy page URL:", page.url)

        print("[11] Trying workspace URL...")
        page.goto("https://share.streamlit.io/workspace", wait_until="domcontentloaded", timeout=15000)
        time.sleep(3)
        save_screenshot(page, "recon_workspace.png")
        print("  Workspace URL:", page.url)

        html2 = page.content()
        with open(os.path.join(SCREENSHOT_DIR, "recon_workspace_source.html"), "w", encoding="utf-8") as f:
            f.write(html2)

        buttons2 = page.query_selector_all("button")
        for i, btn in enumerate(buttons2):
            try:
                text = btn.inner_text()
                visible = btn.is_visible()
                if visible:
                    print(f"  Workspace Button[{i}]: text='{text[:80]}' visible={visible}")
            except Exception:
                pass

    except Exception as e:
        print(f"[ERROR] {e}")
        try:
            save_screenshot(page, "recon_error.png")
        except Exception:
            pass
    finally:
        print("[Done] Closing browser...")
        browser.close()

print("Reconnaissance complete!")

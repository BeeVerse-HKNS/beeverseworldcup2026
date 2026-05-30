import time
from playwright.sync_api import sync_playwright

SCREENSHOT_PATH = r"d:\My_Code_Projects\Harnessing\projects\world-2026\deploy_screenshots\china_debug_check.png"
DIRECT_URL = "https://beeverseworldcup2026.streamlit.app/~/+/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()

    print(f"Navigating directly to app iframe URL: {DIRECT_URL}")
    page.goto(DIRECT_URL, timeout=180000, wait_until="domcontentloaded")
    print(f"Page loaded. Title: {page.title()}")

    print("Waiting for Streamlit app content (polling every 5s, up to 180s)...")
    start = time.time()
    found = False
    while time.time() - start < 180:
        try:
            body_text = page.inner_text("body").strip()
            if body_text and len(body_text) > 50:
                print(f"Content detected after {int(time.time() - start)}s!")
                found = True
                break
        except:
            pass
        time.sleep(5)
        elapsed = int(time.time() - start)
        if elapsed % 15 == 0:
            print(f"  ... still waiting ({elapsed}s)")

    if not found:
        print(f"No substantial content after {int(time.time() - start)}s. Trying stAppViewContainer...")
        try:
            page.wait_for_selector('[data-testid="stAppViewContainer"]', timeout=60000)
            print("stAppViewContainer found!")
            time.sleep(10)
        except:
            print("stAppViewContainer not found either. Taking screenshot of current state.")

    print("Waiting 10s for all content to fully load...")
    time.sleep(10)

    try:
        print("Taking full-page screenshot...")
        page.screenshot(path=SCREENSHOT_PATH, full_page=True)
        print(f"Screenshot saved to {SCREENSHOT_PATH}")
    except Exception as e:
        print(f"Full page screenshot failed: {e}")
        try:
            page.screenshot(path=SCREENSHOT_PATH)
            print(f"Viewport screenshot saved to {SCREENSHOT_PATH}")
        except Exception as e2:
            print(f"All screenshots failed: {e2}")

    print("\n--- Extracting page text content ---")
    try:
        body_text = page.inner_text("body")
        print(body_text[:5000])
    except Exception as e:
        print(f"Error reading body text: {e}")
        body_text = ""

    print("\n--- Looking for version indicator (v:china / v:international) ---")
    all_text_lower = body_text.lower()
    if "v:china" in all_text_lower:
        print(">>> FOUND: v:china in page text")
    elif "v:international" in all_text_lower:
        print(">>> FOUND: v:international in page text")
    else:
        print(">>> No v:china or v:international found in visible text")

    print("\n--- Looking for language selector ---")
    if '简体中文' in body_text:
        print(">>> Language selector shows: 简体中文")
    elif '繁體中文' in body_text:
        print(">>> Language selector shows: 繁體中文")
    elif 'english' in all_text_lower:
        print(">>> Language selector shows: English")
    else:
        print(">>> Could not determine language selector default text")

    print("\n--- Page title ---")
    try:
        print(f"Title: {page.title()}")
    except:
        print("Could not get page title")

    print("\n--- Scanning for version/debug elements ---")
    try:
        all_elements = page.query_selector_all('*')
        for el in all_elements:
            try:
                txt = el.inner_text().strip()
                if txt and len(txt) < 300 and any(kw in txt.lower() for kw in ['v:china', 'v:international', 'app_version', 'version', 'debug']):
                    tag = el.evaluate("e => e.tagName")
                    cls = el.evaluate("e => e.className")
                    print(f"  <{tag}> class='{cls}' text='{txt}'")
            except:
                pass
    except Exception as e:
        print(f"Error scanning elements: {e}")

    print("\n--- Checking sidebar content ---")
    try:
        sidebar = page.query_selector('[data-testid="stSidebar"]')
        if sidebar:
            sidebar_text = sidebar.inner_text()
            print(f"Sidebar text: {sidebar_text[:2000]}")
        else:
            print("No sidebar found")
    except Exception as e:
        print(f"Error reading sidebar: {e}")

    print("\n--- Checking for select dropdowns ---")
    try:
        selects = page.query_selector_all('[data-testid="stSelectbox"]')
        print(f"Found {len(selects)} select boxes")
        for i, sel in enumerate(selects):
            try:
                txt = sel.inner_text()
                print(f"  Select[{i}]: {txt[:300]}")
            except:
                pass
    except Exception as e:
        print(f"Error finding select boxes: {e}")

    print("\n--- Checking HTML source for version constants ---")
    try:
        html_content = page.content()
        for keyword in ['v:china', 'v:international', 'APP_VERSION', 'app_version']:
            idx = html_content.lower().find(keyword.lower())
            if idx >= 0:
                snippet = html_content[max(0, idx-80):idx+150]
                print(f"  Found '{keyword}' in HTML at position {idx}:")
                print(f"    ...{snippet[:250]}...")
    except Exception as e:
        print(f"Error reading HTML: {e}")

    print("\nDone. Closing browser...")
    try:
        browser.close()
        print("Browser closed.")
    except:
        print("Browser already closed.")

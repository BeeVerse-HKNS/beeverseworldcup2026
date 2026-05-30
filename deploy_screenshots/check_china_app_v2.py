import time
from playwright.sync_api import sync_playwright

SCREENSHOT_PATH = r"d:\My_Code_Projects\Harnessing\projects\world-2026\deploy_screenshots\china_debug_check_v2.png"
DIRECT_URL = "https://beeverseworldcup2026.streamlit.app/~/+/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()

    print(f"Navigating to {DIRECT_URL}")
    page.goto(DIRECT_URL, timeout=180000, wait_until="domcontentloaded")

    print("Waiting for content...")
    start = time.time()
    while time.time() - start < 60:
        try:
            body_text = page.inner_text("body").strip()
            if body_text and len(body_text) > 50:
                print(f"Content detected after {int(time.time() - start)}s!")
                break
        except:
            pass
        time.sleep(3)

    time.sleep(10)

    print("\n--- Checking for fixed/absolute positioned elements (version indicator) ---")
    try:
        elements = page.evaluate("""() => {
            const all = document.querySelectorAll('*');
            const results = [];
            for (const el of all) {
                const style = window.getComputedStyle(el);
                const pos = style.position;
                if ((pos === 'fixed' || pos === 'absolute') && style.display !== 'none' && style.visibility !== 'hidden') {
                    const text = el.innerText || el.textContent || '';
                    if (text.trim().length > 0 && text.trim().length < 200) {
                        results.push({
                            tag: el.tagName,
                            position: pos,
                            bottom: style.bottom,
                            right: style.right,
                            text: text.trim(),
                            fontSize: style.fontSize,
                            color: style.color,
                            opacity: style.opacity
                        });
                    }
                }
            }
            return results;
        }""")
        print(f"Found {len(elements)} fixed/absolute positioned elements with text:")
        for el in elements:
            print(f"  <{el['tag']}> pos={el['position']} bottom={el['bottom']} right={el['right']} "
                  f"fontSize={el['fontSize']} color={el['color']} opacity={el['opacity']} "
                  f"text='{el['text']}'")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- Checking for small/hidden text elements ---")
    try:
        small_elements = page.evaluate("""() => {
            const all = document.querySelectorAll('*');
            const results = [];
            for (const el of all) {
                const style = window.getComputedStyle(el);
                const fontSize = parseFloat(style.fontSize);
                const text = (el.innerText || el.textContent || '').trim();
                if (text && fontSize <= 12 && text.length < 200) {
                    results.push({
                        tag: el.tagName,
                        fontSize: style.fontSize,
                        text: text,
                        opacity: style.opacity,
                        color: style.color
                    });
                }
            }
            return results;
        }""")
        print(f"Found {len(small_elements)} small text elements (fontSize <= 12px):")
        for el in small_elements:
            print(f"  <{el['tag']}> fontSize={el['fontSize']} color={el['color']} opacity={el['opacity']} text='{el['text']}'")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- Searching entire HTML for 'china' or 'international' ---")
    try:
        html = page.content()
        for kw in ['china', 'international', 'v:china', 'v:international', 'APP_VERSION', 'app_version']:
            count = html.lower().count(kw.lower())
            if count > 0:
                print(f"  '{kw}' found {count} times in HTML")
                idx = 0
                for _ in range(min(count, 3)):
                    idx = html.lower().find(kw.lower(), idx)
                    if idx >= 0:
                        snippet = html[max(0, idx-100):idx+200]
                        print(f"    at {idx}: ...{snippet[:300]}...")
                        idx += len(kw)
            else:
                print(f"  '{kw}' NOT found in HTML")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- Checking stMarkdown elements for version text ---")
    try:
        markdowns = page.query_selector_all('[data-testid="stMarkdown"]')
        print(f"Found {len(markdowns)} stMarkdown elements")
        for i, md in enumerate(markdowns):
            try:
                txt = md.inner_text()
                if txt.strip():
                    print(f"  Markdown[{i}]: {txt[:200]}")
            except:
                pass
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- Full page text ---")
    try:
        body_text = page.inner_text("body")
        print(body_text[:5000])
    except:
        pass

    print("\nTaking screenshot...")
    try:
        page.screenshot(path=SCREENSHOT_PATH, full_page=True)
        print(f"Screenshot saved to {SCREENSHOT_PATH}")
    except Exception as e:
        print(f"Screenshot error: {e}")

    browser.close()
    print("Done.")

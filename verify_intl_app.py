import json
import re
import time

from playwright.sync_api import sync_playwright


def main():
    url = "https://beeverse-wc2026-international.streamlit.app/"
    screenshot_path = r"d:\My_Code_Projects\Harnessing\projects\world-2026\deploy_screenshots\intl_version_verified.png"

    results = {
        "url": url,
        "screenshot_saved": False,
        "version_international_visible": False,
        "dropdown_language": None,
        "language_option_count": 0,
        "language_options": [],
        "registration_in_english": False,
        "english_indicators_found": [],
        "cookie_consent_banner": False,
        "page_title": None,
        "app_status": None,
        "iframe_text": "",
        "error": None,
    }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                channel="msedge",
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled",
                ],
            )
            context = browser.new_context(
                viewport={"width": 1280, "height": 900},
                java_script_enabled=True,
            )

            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)

            page = context.new_page()

            print(f"[1] Navigating to {url} ...")
            page.goto(url, timeout=120000, wait_until="load")

            print("[2] Waiting for Streamlit iframe to appear (up to 120s) ...")
            for i in range(24):
                time.sleep(5)
                frames = page.frames
                app_frame = None
                for f in frames:
                    if "/~/" in f.url:
                        app_frame = f
                        break

                if app_frame:
                    try:
                        frame_text = app_frame.locator("body").inner_text() or ""
                        if len(frame_text) > 50:
                            print(f"    Attempt {i+1}: iframe loaded! text_len={len(frame_text)}")
                            break
                    except Exception:
                        pass

                print(f"    Attempt {i+1}/24: iframe not ready yet, frames={len(frames)}")

            print("[3] Extra 15s wait for widgets ...")
            time.sleep(15)

            print("[4] Taking full-page screenshot ...")
            page.screenshot(path=screenshot_path, full_page=True)
            results["screenshot_saved"] = True

            results["page_title"] = page.title()

            app_frame = None
            for f in page.frames:
                if "/~/" in f.url:
                    app_frame = f
                    break

            iframe_text = ""
            if app_frame:
                try:
                    iframe_text = app_frame.locator("body").inner_text() or ""
                except Exception:
                    pass

            results["iframe_text"] = iframe_text

            print(f"[5] Iframe text ({len(iframe_text)} chars):")
            print(iframe_text[:500])

            if iframe_text and "Version" in iframe_text:
                results["app_status"] = "RUNNING"
            else:
                results["app_status"] = "PARTIAL"

            print("[6] Checking Version: international ...")
            results["version_international_visible"] = "Version: international" in iframe_text
            print(f"    version_international_visible = {results['version_international_visible']}")

            print("[7] Getting language dropdown options from iframe ...")
            if app_frame:
                iframe_html = app_frame.content()
                
                option_matches = re.findall(r'<option[^>]*value="([^"]*)"[^>]*>([^<]*)</option>', iframe_html)
                if option_matches:
                    results["language_options"] = [opt[1] for opt in option_matches]
                    results["language_option_count"] = len(option_matches)
                    print(f"    Found {len(option_matches)} options via HTML: {results['language_options']}")

                for sel in [
                    "select[aria-label='Language']",
                    "select[aria-label='language']",
                    "select",
                    "[data-testid='stSelect']",
                    ".stSelect",
                ]:
                    try:
                        loc = app_frame.locator(sel).first
                        if loc.is_visible(timeout=3000):
                            results["dropdown_language"] = loc.get_attribute("aria-label")
                            try:
                                opts = loc.locator("option").all()
                                if opts:
                                    results["language_option_count"] = len(opts)
                                    results["language_options"] = [o.inner_text() for o in opts]
                            except Exception:
                                pass
                            print(f"    Found select: {sel}, label={results['dropdown_language']}, options={results['language_options']}")
                            break
                    except Exception:
                        continue

                if not results["language_options"]:
                    print("    Trying to click the language dropdown to reveal options ...")
                    try:
                        lang_label = app_frame.locator("text=Language").first
                        if lang_label.is_visible(timeout=3000):
                            print("    Found 'Language' text label")
                    except Exception:
                        pass

                    try:
                        select_container = app_frame.locator("[data-baseweb='select']").first
                        if select_container.is_visible(timeout=3000):
                            print("    Found baseweb select container, clicking ...")
                            select_container.click()
                            time.sleep(2)

                            listbox = app_frame.locator("[role='listbox'], [data-baseweb='popover']")
                            if listbox.count() > 0:
                                items = listbox.first.locator("[role='option']").all()
                                results["language_option_count"] = len(items)
                                results["language_options"] = [item.inner_text() for item in items]
                                print(f"    Found {len(items)} options via listbox: {results['language_options']}")
                            else:
                                print("    No listbox found after clicking")
                    except Exception as e:
                        print(f"    Error clicking select: {e}")

            print("[8] Checking registration form language ...")
            all_text = iframe_text
            english_indicators = [
                "Registration",
                "Full Name",
                "Email",
                "Submit",
                "Register",
                "First Name",
                "Last Name",
                "Phone",
                "Country",
                "Select Language",
                "World Cup",
                "Predictor",
                "Please register",
                "Name",
                "Welcome",
                "Enter",
            ]
            english_found = [ind for ind in english_indicators if ind in all_text]
            results["english_indicators_found"] = english_found
            results["registration_in_english"] = len(english_found) >= 2

            print("[9] Checking cookie consent ...")
            for ind in ["cookie", "Cookie", "consent", "Consent", "We use cookies",
                        "This site uses cookies", "Accept all", "Manage cookies"]:
                if ind in all_text or ind in page.content():
                    results["cookie_consent_banner"] = True
                    break

            print("[10] Closing ...")
            browser.close()

    except Exception as e:
        results["error"] = str(e)
        print(f"[ERROR] {e}")

    print("\n===== FINAL RESULTS =====")
    safe = {k: v for k, v in results.items() if k != "iframe_text"}
    print(json.dumps(safe, indent=2, ensure_ascii=False))

    if results.get("iframe_text"):
        print("\n===== FULL IFRAME TEXT =====")
        print(results["iframe_text"])

    return results


if __name__ == "__main__":
    main()

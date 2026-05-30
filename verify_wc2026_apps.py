import json
import re
import time
from datetime import datetime

from playwright.sync_api import sync_playwright


SCREENSHOT_DIR = r"d:\My_Code_Projects\Harnessing\projects\world-2026\deploy_screenshots"

APPS = [
    {
        "name": "China Version",
        "url": "https://beeverseworldcup2026.streamlit.app/",
        "expected_default_code": "+86",
        "expected_language_indicators": ["注册", "手机号", "姓名", "提交", "邮箱"],
        "screenshot_prefix": "verify_china",
    },
    {
        "name": "International Version",
        "url": "https://beeverse-wc2026-international.streamlit.app/",
        "expected_default_code": "+1",
        "expected_language_indicators": ["Registration", "Phone", "Name", "Submit", "Email"],
        "screenshot_prefix": "verify_intl",
    },
]


def verify_app(app_config):
    url = app_config["url"]
    app_name = app_config["name"]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_landing = f"{SCREENSHOT_DIR}\\{app_config['screenshot_prefix']}_{ts}_landing.png"
    screenshot_form = f"{SCREENSHOT_DIR}\\{app_config['screenshot_prefix']}_{ts}_form.png"

    results = {
        "app_name": app_name,
        "url": url,
        "timestamp": ts,
        "app_loaded": False,
        "screenshot_landing_saved": False,
        "screenshot_form_saved": False,
        "registration_form_visible": False,
        "country_code_dropdown_visible": False,
        "default_country_code": None,
        "expected_default_code": app_config["expected_default_code"],
        "default_code_correct": False,
        "language_indicators_found": [],
        "iframe_text_length": 0,
        "page_title": None,
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

            print(f"\n{'='*60}")
            print(f"Verifying: {app_name}")
            print(f"URL: {url}")
            print(f"{'='*60}")

            print(f"[1] Navigating to {url} ...")
            page.goto(url, timeout=120000, wait_until="load")

            print("[2] Waiting for Streamlit iframe to appear (up to 120s) ...")
            app_frame = None
            for i in range(24):
                time.sleep(5)
                frames = page.frames
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

            print("[3] Extra 15s wait for widgets to render ...")
            time.sleep(15)

            print("[4] Taking landing page screenshot ...")
            page.screenshot(path=screenshot_landing, full_page=True)
            results["screenshot_landing_saved"] = True

            results["page_title"] = page.title()

            if not app_frame:
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

            results["iframe_text_length"] = len(iframe_text)

            print(f"[5] Iframe text ({len(iframe_text)} chars):")
            print(iframe_text[:800])

            if iframe_text and len(iframe_text) > 100:
                results["app_loaded"] = True

            print("[6] Checking registration form visibility ...")
            registration_indicators = ["注册", "Registration", "Register", "手机", "Phone",
                                       "姓名", "Name", "邮箱", "Email", "Submit", "提交"]
            found_indicators = [ind for ind in registration_indicators if ind in iframe_text]
            results["registration_form_visible"] = len(found_indicators) >= 2
            print(f"    Registration indicators found: {found_indicators}")

            print("[7] Checking language indicators ...")
            lang_found = [ind for ind in app_config["expected_language_indicators"] if ind in iframe_text]
            results["language_indicators_found"] = lang_found
            print(f"    Language indicators: {lang_found}")

            print("[8] Checking country code dropdown ...")
            if app_frame:
                iframe_html = app_frame.content()

                country_code_patterns = [
                    r'\+86',
                    r'\+1',
                    r'\+852',
                    r'\+44',
                    r'\+81',
                    r'\+82',
                    r'\+33',
                    r'\+49',
                    r'\+61',
                    r'\+65',
                    r'\+91',
                    r'\+55',
                    r'\+7',
                    r'\+34',
                    r'\+39',
                    r'\+31',
                ]
                codes_in_html = []
                for pattern in country_code_patterns:
                    if re.search(pattern, iframe_html):
                        codes_in_html.append(pattern.replace(r'\+', '+'))
                print(f"    Country codes found in HTML: {codes_in_html}")

                select_elements = app_frame.locator("select").all()
                print(f"    Total <select> elements: {len(select_elements)}")

                baseweb_selects = app_frame.locator("[data-baseweb='select']").all()
                print(f"    Baseweb select elements: {len(baseweb_selects)}")

                for i, sel in enumerate(select_elements):
                    try:
                        aria_label = sel.get_attribute("aria-label") or ""
                        opts = sel.locator("option").all()
                        opt_texts = [o.inner_text() for o in opts]
                        opt_values = [o.get_attribute("value") for o in opts]
                        print(f"    Select[{i}]: aria-label='{aria_label}', options={opt_texts[:10]}, values={opt_values[:10]}")

                        has_country_code = any("+" in t for t in opt_texts)
                        if has_country_code or "country" in aria_label.lower() or "code" in aria_label.lower() or "国家" in aria_label or "代码" in aria_label:
                            results["country_code_dropdown_visible"] = True
                            for opt_text in opt_texts:
                                if "+" in opt_text:
                                    results["default_country_code"] = opt_text
                                    break
                            if not results["default_country_code"] and opt_texts:
                                results["default_country_code"] = opt_texts[0]
                            print(f"    >>> Country code dropdown found! Default: {results['default_country_code']}")
                    except Exception as e:
                        print(f"    Select[{i}] error: {e}")

                if not results["country_code_dropdown_visible"]:
                    print("    Trying baseweb select approach ...")
                    for i, bsel in enumerate(baseweb_selects):
                        try:
                            if bsel.is_visible(timeout=3000):
                                bsel_text = bsel.inner_text()
                                print(f"    Baseweb select[{i}]: text='{bsel_text[:200]}'")

                                if "+" in bsel_text:
                                    results["country_code_dropdown_visible"] = True
                                    code_match = re.search(r'(\+\d+)', bsel_text)
                                    if code_match:
                                        results["default_country_code"] = code_match.group(1)
                                    print(f"    >>> Country code found in baseweb select! Default: {results['default_country_code']}")
                                    break
                        except Exception as e:
                            print(f"    Baseweb select[{i}] error: {e}")

                if not results["country_code_dropdown_visible"]:
                    print("    Trying text search in iframe ...")
                    phone_section = ""
                    if "手机" in iframe_text or "Phone" in iframe_text or "phone" in iframe_text.lower():
                        phone_idx = -1
                        for marker in ["手机", "Phone", "phone"]:
                            idx = iframe_text.find(marker)
                            if idx >= 0:
                                phone_idx = idx
                                break
                        if phone_idx >= 0:
                            phone_section = iframe_text[max(0, phone_idx-100):phone_idx+200]
                            print(f"    Phone section context: '{phone_section[:300]}'")

                            code_match = re.search(r'(\+\d{1,4})', phone_section)
                            if code_match:
                                results["country_code_dropdown_visible"] = True
                                results["default_country_code"] = code_match.group(1)
                                print(f"    >>> Country code found near phone field: {results['default_country_code']}")

                if not results["country_code_dropdown_visible"]:
                    print("    Trying to click baseweb select to reveal dropdown ...")
                    try:
                        select_containers = app_frame.locator("[data-baseweb='select']").all()
                        for i, sc in enumerate(select_containers):
                            try:
                                if sc.is_visible(timeout=2000):
                                    sc.click()
                                    time.sleep(2)

                                    listbox = app_frame.locator("[role='listbox'], [data-baseweb='popover']")
                                    if listbox.count() > 0:
                                        items = listbox.first.locator("[role='option']").all()
                                        item_texts = [item.inner_text() for item in items]
                                        print(f"    Listbox items from select[{i}]: {item_texts[:15]}")

                                        has_country_code = any("+" in t for t in item_texts)
                                        if has_country_code:
                                            results["country_code_dropdown_visible"] = True
                                            for t in item_texts:
                                                if "+" in t:
                                                    code_match = re.search(r'(\+\d+)', t)
                                                    if code_match:
                                                        results["default_country_code"] = code_match.group(1)
                                                        break
                                            break
                            except Exception:
                                continue
                    except Exception as e:
                        print(f"    Click approach error: {e}")

                if not results["country_code_dropdown_visible"] and codes_in_html:
                    results["country_code_dropdown_visible"] = True
                    results["default_country_code"] = codes_in_html[0]
                    print(f"    >>> Country codes found in HTML (fallback): {codes_in_html}")

            if results["default_country_code"]:
                expected = app_config["expected_default_code"]
                results["default_code_correct"] = results["default_country_code"] == expected
                if not results["default_code_correct"]:
                    print(f"    WARNING: Expected '{expected}', got '{results['default_country_code']}'")

            print("[9] Taking form screenshot ...")
            try:
                page.screenshot(path=screenshot_form, full_page=True)
                results["screenshot_form_saved"] = True
            except Exception as e:
                print(f"    Form screenshot error: {e}")

            print("[10] Closing browser ...")
            browser.close()

    except Exception as e:
        results["error"] = str(e)
        print(f"[ERROR] {e}")

    return results


def main():
    all_results = []

    for app in APPS:
        result = verify_app(app)
        all_results.append(result)

    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)

    for r in all_results:
        print(f"\n--- {r['app_name']} ---")
        print(f"  URL: {r['url']}")
        print(f"  App Loaded: {'✅ YES' if r['app_loaded'] else '❌ NO'}")
        print(f"  Registration Form Visible: {'✅ YES' if r['registration_form_visible'] else '❌ NO'}")
        print(f"  Country Code Dropdown Visible: {'✅ YES' if r['country_code_dropdown_visible'] else '❌ NO'}")
        print(f"  Default Country Code: {r['default_country_code'] or 'NOT FOUND'}")
        print(f"  Expected Default Code: {r['expected_default_code']}")
        print(f"  Default Code Correct: {'✅ YES' if r['default_code_correct'] else '❌ NO'}")
        print(f"  Language Indicators: {r['language_indicators_found']}")
        print(f"  Landing Screenshot: {'✅ Saved' if r['screenshot_landing_saved'] else '❌ Not saved'}")
        print(f"  Form Screenshot: {'✅ Saved' if r['screenshot_form_saved'] else '❌ Not saved'}")
        if r['error']:
            print(f"  Error: {r['error']}")

    report_path = f"{SCREENSHOT_DIR}\\verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"\nReport saved to: {report_path}")

    return all_results


if __name__ == "__main__":
    main()

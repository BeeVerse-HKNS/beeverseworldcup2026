import asyncio
import os
import json
from playwright.async_api import async_playwright

SCREENSHOT_DIR = r"d:\My_Code_Projects\Harnessing\projects\world-2026-deploy\deploy_screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        print("[1] Navigating to Streamlit Cloud...")
        await page.goto("https://share.streamlit.io/", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(5)

        url = page.url
        print(f"Current URL: {url}")

        if "login" in url.lower() or "auth" in url.lower() or "accounts.streamlit.io" in url.lower() or "authkit" in url.lower():
            print("[LOGIN REQUIRED] Please log in manually in the browser window.")
            print("Waiting up to 120 seconds for login...")
            await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "inspect_login.png"), full_page=True)

            for i in range(60):
                await asyncio.sleep(2)
                cur = page.url
                if "share.streamlit.io" in cur and "login" not in cur.lower() and "auth" not in cur.lower() and "authkit" not in cur.lower():
                    print(f"Login detected! URL: {cur}")
                    break
            else:
                print("Login timeout!")
                await browser.close()
                return

        await asyncio.sleep(3)
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "inspect_dashboard.png"), full_page=True)

        html = await page.content()
        with open(os.path.join(SCREENSHOT_DIR, "dashboard_page.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Saved dashboard HTML ({len(html)} chars)")

        all_buttons = await page.query_selector_all("button")
        print(f"\nFound {len(all_buttons)} buttons:")
        for i, btn in enumerate(all_buttons):
            try:
                text = (await btn.text_content() or "").strip()[:100]
                href = await btn.get_attribute("href") or ""
                cls = await btn.get_attribute("class") or ""
                print(f"  Button[{i}]: text='{text}' class='{cls[:80]}' href='{href}'")
            except Exception:
                pass

        all_links = await page.query_selector_all("a")
        print(f"\nFound {len(all_links)} links:")
        for i, link in enumerate(all_links):
            try:
                text = (await link.text_content() or "").strip()[:100]
                href = await link.get_attribute("href") or ""
                print(f"  Link[{i}]: text='{text}' href='{href}'")
            except Exception:
                pass

        all_inputs = await page.query_selector_all("input")
        print(f"\nFound {len(all_inputs)} inputs:")
        for i, inp in enumerate(all_inputs):
            try:
                itype = await inp.get_attribute("type") or ""
                name = await inp.get_attribute("name") or ""
                placeholder = await inp.get_attribute("placeholder") or ""
                aria_label = await inp.get_attribute("aria-label") or ""
                cls = await inp.get_attribute("class") or ""
                print(f"  Input[{i}]: type='{itype}' name='{name}' placeholder='{placeholder}' aria-label='{aria_label}' class='{cls[:80]}'")
            except Exception:
                pass

        print("\n[2] Navigating to deploy page...")
        await page.goto("https://share.streamlit.io/deploy", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(5)
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "inspect_deploy.png"), full_page=True)

        html2 = await page.content()
        with open(os.path.join(SCREENSHOT_DIR, "deploy_page.html"), "w", encoding="utf-8") as f:
            f.write(html2)
        print(f"Saved deploy page HTML ({len(html2)} chars)")

        all_buttons2 = await page.query_selector_all("button")
        print(f"\nDeploy page - Found {len(all_buttons2)} buttons:")
        for i, btn in enumerate(all_buttons2):
            try:
                text = (await btn.text_content() or "").strip()[:100]
                cls = await btn.get_attribute("class") or ""
                print(f"  Button[{i}]: text='{text}' class='{cls[:80]}'")
            except Exception:
                pass

        all_inputs2 = await page.query_selector_all("input")
        print(f"\nDeploy page - Found {len(all_inputs2)} inputs:")
        for i, inp in enumerate(all_inputs2):
            try:
                itype = await inp.get_attribute("type") or ""
                name = await inp.get_attribute("name") or ""
                placeholder = await inp.get_attribute("placeholder") or ""
                aria_label = await inp.get_attribute("aria-label") or ""
                print(f"  Input[{i}]: type='{itype}' name='{name}' placeholder='{placeholder}' aria-label='{aria_label}'")
            except Exception:
                pass

        all_selects = await page.query_selector_all("select, [role='combobox'], [role='listbox']")
        print(f"\nDeploy page - Found {len(all_selects)} select/combo elements:")
        for i, sel in enumerate(all_selects):
            try:
                tag = await sel.evaluate("el => el.tagName")
                role = await sel.get_attribute("role") or ""
                cls = await sel.get_attribute("class") or ""
                text = (await sel.text_content() or "").strip()[:100]
                print(f"  Select[{i}]: tag='{tag}' role='{role}' text='{text}' class='{cls[:80]}'")
            except Exception:
                pass

        print("\n[3] Trying direct deploy URL with params...")
        deploy_url = f"https://share.streamlit.io/deploy?repository=BeeVerse-HKNS%2Fworld-cup-2026-predictor&branch=main&mainFile=streamlit_app.py"
        await page.goto(deploy_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(5)
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "inspect_direct_deploy.png"), full_page=True)

        html3 = await page.content()
        with open(os.path.join(SCREENSHOT_DIR, "direct_deploy_page.html"), "w", encoding="utf-8") as f:
            f.write(html3)
        print(f"Saved direct deploy page HTML ({len(html3)} chars)")

        all_buttons3 = await page.query_selector_all("button")
        print(f"\nDirect deploy - Found {len(all_buttons3)} buttons:")
        for i, btn in enumerate(all_buttons3):
            try:
                text = (await btn.text_content() or "").strip()[:100]
                cls = await btn.get_attribute("class") or ""
                print(f"  Button[{i}]: text='{text}' class='{cls[:80]}'")
            except Exception:
                pass

        all_inputs3 = await page.query_selector_all("input")
        print(f"\nDirect deploy - Found {len(all_inputs3)} inputs:")
        for i, inp in enumerate(all_inputs3):
            try:
                itype = await inp.get_attribute("type") or ""
                name = await inp.get_attribute("name") or ""
                placeholder = await inp.get_attribute("placeholder") or ""
                value = await inp.get_attribute("value") or ""
                aria_label = await inp.get_attribute("aria-label") or ""
                print(f"  Input[{i}]: type='{itype}' name='{name}' placeholder='{placeholder}' value='{value}' aria-label='{aria_label}'")
            except Exception:
                pass

        print("\nInspection complete. Check the HTML files and screenshots.")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())

from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    
    page.goto('http://localhost:8501')
    page.wait_for_load_state('networkidle')
    time.sleep(8)
    
    page.screenshot(path='d:/My_Code_Projects/Harnessing/projects/world-2026/qa_01_registration.png', full_page=True)
    print("Screenshot 1: Registration page saved")
    
    content = page.content()
    
    has_gambling = any(term in content for term in ['Betting Odds', 'Bookmaker', '博彩公司', 'betting_odds'])
    print(f"Gambling terminology found: {has_gambling}")
    
    has_statistical = 'Statistical Probability' in content or '統計概率' in content or '统计概率' in content
    print(f"Statistical probability text found: {has_statistical}")
    
    has_register = 'register' in content.lower() or '註冊' in content or '注册' in content
    print(f"Registration form found: {has_register}")
    
    has_dark_bg = '1A1A2E' in content or '16213E' in content
    print(f"Dark theme CSS found: {has_dark_bg}")
    
    all_inputs = page.locator('input').all()
    print(f"Total input fields found: {len(all_inputs)}")
    
    for i, inp in enumerate(all_inputs):
        aria = inp.get_attribute('aria-label') or ''
        placeholder = inp.get_attribute('placeholder') or ''
        print(f"  Input {i}: aria-label='{aria}', placeholder='{placeholder}'")
    
    all_buttons = page.locator('button').all()
    print(f"Total buttons found: {len(all_buttons)}")
    for i, btn in enumerate(all_buttons[:10]):
        text = btn.inner_text()
        print(f"  Button {i}: '{text}'")
    
    if len(all_inputs) >= 3:
        all_inputs[0].fill("Test User")
        all_inputs[1].fill("test@example.com")
        all_inputs[2].fill("+852 1234 5678")
        print("Filled registration form")
        
        for btn in all_buttons:
            text = btn.inner_text()
            if 'Enter' in text or '進入' in text or '进入' in text:
                btn.click()
                print(f"Clicked button: '{text}'")
                break
        
        time.sleep(8)
        page.screenshot(path='d:/My_Code_Projects/Harnessing/projects/world-2026/qa_02_after_registration.png', full_page=True)
        print("Screenshot 2: After registration saved")
    
    page.screenshot(path='d:/My_Code_Projects/Harnessing/projects/world-2026/qa_03_main_app.png', full_page=True)
    print("Screenshot 3: Main app saved")
    
    sidebar = page.locator('[data-testid="stSidebar"]')
    if sidebar.count() > 0:
        sidebar_text = sidebar.first.inner_text()
        print(f"\nSidebar content (first 800 chars):\n{sidebar_text[:800]}")
        
        has_team_squads = 'Team Squads' in sidebar_text or '球隊陣容' in sidebar_text or '球队阵容' in sidebar_text
        print(f"\nTeam Squads tab found: {has_team_squads}")
        
        has_theme_toggle = 'Dark' in sidebar_text or '深色' in sidebar_text or 'Theme' in sidebar_text or '主題' in sidebar_text
        print(f"Theme toggle found: {has_theme_toggle}")
    else:
        has_team_squads = False
        has_theme_toggle = False
    
    print("\n=== QA SUMMARY ===")
    print(f"1. Registration gate: {'PASS' if has_register else 'FAIL'}")
    print(f"2. No gambling terms: {'PASS' if not has_gambling else 'FAIL'}")
    print(f"3. Statistical probability: {'PASS' if has_statistical else 'FAIL'}")
    print(f"4. Dark theme CSS: {'PASS' if has_dark_bg else 'FAIL'}")
    print(f"5. Team Squads tab: {'PASS' if has_team_squads else 'FAIL'}")
    print(f"6. Theme toggle: {'PASS' if has_theme_toggle else 'FAIL'}")
    
    browser.close()

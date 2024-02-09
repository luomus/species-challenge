from playwright.sync_api import sync_playwright


def test_anon_user(browser):
    page = browser.new_page()

    front_page_text = "Havaitsetko 100 lajia"

    # Access pages that are publicly available
    page.goto("http://web:8081")
    assert "Kirjaudu sisään" in page.content()

    page.click("text=Sienihaaste 2024 Playwright")
    assert "Playwright-paikka" in page.content()
    assert "Osallistujat ovat havainneet yhteensä" in page.content()

    # Access pages that require login
    # Access own participations page
    page.goto("http://web:8081/oma")
    assert "Kirjaudu ensin sisään" in page.content()
    assert front_page_text in page.content()

    # Access a participation
    page.goto("http://web:8081/tilasto/5/35")
    assert "Kirjaudu ensin sisään" in page.content()
    assert front_page_text in page.content()    

    # Access admin page
    page.goto("http://web:8081/admin")
    assert front_page_text in page.content()

    # Edit a challenge
    page.goto("http://web:8081/admin/haaste/5")
    assert front_page_text in page.content()

    # Edit a participation
    page.goto("http://web:8081/osallistuminen/5/35")
    assert "Kirjaudu ensin sisään" in page.content()
    assert front_page_text in page.content()

    page.close()


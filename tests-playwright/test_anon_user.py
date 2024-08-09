from playwright.sync_api import sync_playwright


# Access pages that are publicly available
def test_anon_public_pages(browser):
    page = browser.new_page()

    front_page_text = "Havaitsetko 100 lajia"

    # Access front page
    page.goto("http://web:8081")
    assert "Kirjaudu sisään" in page.content()

    # Access challenge page
    page.click("text=Sienihaaste 2024 Playwright")
    assert "Playwright-paikka" in page.content()
    assert "Osallistujat ovat havainneet yhteensä" in page.content()

    # Access a challenge that doesn't exist, which should redirect to front page
    page.goto("http://web:8081/haaste/99")
    assert front_page_text in page.content()


# Access pages that require login
def test_anon_restricted_pages(browser):
    page = browser.new_page()

    front_page_text = "Havaitsetko 100 lajia"

    # Access own participations page, which should redirect to front page
    page.goto("http://web:8081/oma")
    assert "Kirjaudu ensin sisään" in page.content()
    assert front_page_text in page.content()

    # Access a participation, which should redirect to front page
    page.goto("http://web:8081/tilasto/5/35")
    assert "Kirjaudu ensin sisään" in page.content()
    assert front_page_text in page.content()    

    # Access admin page, which should redirect to front page
    page.goto("http://web:8081/admin")
    assert front_page_text in page.content()

    # Edit a challenge, which should redirect to front page
    page.goto("http://web:8081/admin/haaste/5")
    assert front_page_text in page.content()

    # Edit a participation, which should redirect to front page
    page.goto("http://web:8081/osallistuminen/5/35")
    assert "Kirjaudu ensin sisään" in page.content()
    assert front_page_text in page.content()

    page.close()


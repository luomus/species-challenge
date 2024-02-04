from playwright.sync_api import sync_playwright


def test_anon_user(browser):
    page = browser.new_page()

    # Access pages that are publicly available
    page.goto("http://web:8081")
    assert "100 Lajia -haasteet" in page.content()

    page.goto("http://web:8081/haaste/4")
    assert "Nimi Merkkinen" in page.content()
    assert "Osallistujat ovat havainneet yhteensä" in page.content()

    # Access pages that require login
    # Access own participations page
    page.goto("http://web:8081/oma")
    assert "Kirjaudu ensin sisään" in page.content()
    assert "100 Lajia -haasteet" in page.content()

    # Access admin page
    page.goto("http://web:8081/admin")
    assert "100 Lajia -haasteet" in page.content()

    # Edit a challenge
    page.goto("http://web:8081/admin/haaste/4")
    assert "100 Lajia -haasteet" in page.content()

    # Edit a participation
    page.goto("http://web:8081/osallistuminen/4/5")
    assert "Kirjaudu ensin sisään" in page.content()
    assert "100 Lajia -haasteet" in page.content()

    page.close()


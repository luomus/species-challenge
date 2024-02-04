
def test_challenge_participants(browser):
    page = browser.new_page()
    page.goto("http://web:8081/haaste/4")
    assert "Nimi Merkkinen" in page.content()
    assert "Osallistujat ovat havainneet yhteensä" in page.content()
    page.close()

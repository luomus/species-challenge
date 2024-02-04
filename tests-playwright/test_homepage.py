from playwright.sync_api import sync_playwright

def test_homepage_loads(browser):
    page = browser.new_page()
    page.goto("http://web:8081")
    assert "100 Lajia -haasteet" in page.content()
    page.close()

from playwright.sync_api import sync_playwright

import pytest
import os

from urllib.parse import urljoin, urlparse, parse_qs


def extract_token(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    token = query_params.get('token', [None])[0]
    return token


# Login ans save login state
def test_login_and_save_state(browser):
    context = browser.new_context()
    page = context.new_page()

# Debug helpers
#    page.on('request', lambda request: print('----> Request URL:', request.url))
#    page.on('response', lambda response: print(f'      Response URL: {response.url}, Status: {response.status}'))

    lajifi_username = os.environ.get("LAJIFI_SC_ADMIN_USERNAME")
    lajifi_password = os.environ.get("LAJIFI_SC_ADMIN_PASSWORD")

    page.goto("http://web:8081")
    
    # Step 1: Find link and navigate to the login page
    login_link_locator = page.locator('li#login a')
    login_link_href = login_link_locator.get_attribute('href')

    page.goto("http://web:8081" + login_link_href)
    assert "Haasteisiin osallistuminen vaatii kirjautumista" in page.content()

    # Step 2: Navigate to auth system
    login_link_locator = page.locator('p#login_p a')
    login_link_href = login_link_locator.get_attribute('href')

    page.goto(login_link_href)
    assert "Käytä Laji.fi-tunnusta" in page.content()

    # Step 3: Click Laji.fi login link
    login_link_locator = page.locator('a#local-login')
    login_link_href = login_link_locator.get_attribute('href')
    absolute_url = absolute_url = urljoin(page.url, login_link_href)
    page.goto(absolute_url)
    assert "Kirjaudu sisään Laji.fi-tunnuksella" in page.content()

    # Step 4: Fill in the login form
    page.wait_for_selector('input[name="password"]')

    page.fill("input[name='email']", lajifi_username)
    page.fill("input[name='password']", lajifi_password)
    
    # Step 5: Submit the form
    page.click("button.submit")

    # Issue: Playwright cannot follow these login redirections, but gets stuck at /login.
    # Workaround: extract token and navigate to /login manually.
    token = extract_token(page.url)    
    page.goto("http://web:8081/login?token=" + token)

    page.wait_for_selector('#logout')

    # Save the authentication state to a file (/tests-playgright/state_admin.json)
    context.storage_state(path='state_admin.json')

    # Wait for the state to be saved
    page.wait_for_timeout(3000)

    page.close()


# Access pages as logged in user
def test_admin_edits(browser):
    context = browser.new_context(storage_state='state_admin.json')
    page = context.new_page()

    # Access front page, which should have link to admin page
    page.goto("http://web:8081")
    assert "Admin" in page.content()

    # Access admin page, which should have test challenges
    page.goto("http://web:8081/admin")
    assert "<h1>Admin</h1>" in page.content()
    assert "Luonnos Playwright" in page.content()
    assert "Suljettu Playwright" in page.content()

    # Access challenge edit page
    page.click("#challenge_12 .button")
    assert "<h1>Haasteen muokkaus: Luonnos Playwright</h1>" in page.content()

    # Replace text in #description field
    random_text = f"Playwright testi {os.urandom(8).hex()}"
    page.fill("#description", random_text)

    # Click button type="submit"
    page.click("button[type='submit']")

    # Check that the edit was successful
    page.wait_for_selector(".flash")
    assert "Haaste on nyt tallennettu" in page.content()
    assert random_text in page.content()

    # Try to access challenge that does not exist
    page.goto("http://web:8081/admin/haaste/999")
    page.wait_for_selector(".flash")
    assert "Haastetta ei löytynyt" in page.content()


# Logout and tear down state
def test_teardown(browser):
    state_file = 'state_admin.json'
    context = browser.new_context(storage_state='state_admin.json')
    page = context.new_page()

    # Click logout, which should redirect to front page with logout flash message
    page.goto("http://web:8081/oma")
    page.click("#logout a")
    print(page.url)
    page.wait_for_selector('#body_home')
    assert "Olet kirjautunut ulos." in page.content()

    # Try to access admin page, which should redirect to front page
    page.goto("http://web:8081/admin")
    page.wait_for_selector('#body_home')
    assert "Kirjaudu sisään" in page.content()

    os.remove(state_file)
    

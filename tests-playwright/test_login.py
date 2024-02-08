
from playwright.sync_api import sync_playwright

import pytest
import os

from urllib.parse import urljoin, urlparse, parse_qs

def extract_token(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    token = query_params.get('token', [None])[0]
    return token


def test_login_and_save_state(browser):
    context = browser.new_context()
    page = context.new_page()

# Debug helpers
#    page.on('request', lambda request: print('----> Request URL:', request.url))
#    page.on('response', lambda response: print(f'      Response URL: {response.url}, Status: {response.status}'))

    lajifi_username = os.environ.get("LAJIFI_USERNAME")
    lajifi_password = os.environ.get("LAJIFI_PASSWORD")

    page.goto("http://web:8081")
    
    # Step 1: Navigate to the login page
    login_link_locator = page.locator('span#login a')
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

    # Issue: Playwright cannot follow redirections, but gets stuck at /login.
    # Workaround: extract token and navigate to /login manually.
    token = extract_token(page.url)
    page.goto("http://web:8081/login?token=" + token)

    page.wait_for_selector('#logout')
    
    # Save the authentication state to a file
    context.storage_state(path='state.json')

    # Wait for the state to be saved
    page.wait_for_timeout(3000)

    page.close()


def test_own_data(browser):
    context = browser.new_context(storage_state='state.json')
    page = context.new_page()

# Debug helpers
#    page.on('request', lambda request: print('----> Request URL:', request.url))
#    page.on('response', lambda response: print(f'      Response URL: {response.url}, Status: {response.status}'))

    # Check own data of the logged in user
    page.goto("http://web:8081")
    assert "Omat osallistumiset" in page.content()

    page.goto("http://web:8081/oma")
    assert "<h1>Omat osallistumiset</h1>" in page.content()


def test_add_edit_participation(browser):
    context = browser.new_context(storage_state='state.json')
    page = context.new_page()

    # Challenge where this person has not participated in
    page.goto("http://web:8081/haaste/5")
    assert "Et ole osallistunut tähän haasteeseen" in page.content()

    # Add participation
    page.click("#add_participation")
    assert "Osallistuminen haasteeseen Sienihaaste" in page.content()

    # Fill in fields
    page.fill("input[name='name']", "Playwright")
    page.fill("#place", "Näyttämö")

    # Add taxa
    # Todo: click taxon name to add it to the form
    page.fill("#MX_43922", "2024-01-01")
    page.fill("#MX_43502", "2024-01-02")

    # Submit the form
    page.click("#submit_button")

    # Check that the participation was added
    page.wait_for_selector(".flash")
    assert "Osallistumisesi on nyt tallennettu" in page.content()
    assert "2 lajia" in page.content()

    # Remove taxon
    page.fill("#MX_43922", "")

    # Submit the form
    page.click("#submit_button")
    
    # Check that the edit was successful
    page.wait_for_selector(".flash")
    assert "Osallistumisesi on nyt tallennettu" in page.content()
    assert "1 lajia" in page.content()

    # Check that field #MX_43922 value is empty
    assert page.input_value("#MX_43922") == ""

    # Trash the participation
    page.click("#trash_button")
    page.click("#confirm_button")

    # Check that trash was successful
    page.wait_for_selector(".flash")
    assert "Osallistumisesi on nyt tallennettu" in page.content()
    assert page.input_value("#trashed") == "1"

    # Check that trashed participation is not visible
    page.goto("http://web:8081/haaste/5")
    assert "Et ole osallistunut tähän haasteeseen" in page.content()


def test_teardown():
    state_file = 'state.json'
    os.remove(state_file)
    


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

    # Save the authentication state to a file (/tests-playgright/state.json)
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

    # Access front page, which should have link to own participations
    page.goto("http://web:8081")
    assert "Omat osallistumiset" in page.content()

    # Access own participations page, which should have test participation
    page.goto("http://web:8081/oma")
    assert "<h1>Omat osallistumiset</h1>" in page.content()
    assert "Teppo Playwright" in page.content()


def test_add_edit_participation(browser):
    context = browser.new_context(storage_state='state.json')
    page = context.new_page()

    # ----------------------------------------------
    # Access challenge this person hasn't participated in 
    page.goto("http://web:8081/haaste/5")
    assert "Et ole osallistunut tähän haasteeseen" in page.content()

    # ----------------------------------------------
    # Set up own participation
    # Access participation adding page
    page.click("#add_participation")
    assert "Osallistuminen: Sienihaaste" in page.content()

    # Fill in fields
    page.fill("input[name='name']", "Playwright")
    page.fill("#place", "Näyttämö")

    # Add taxa in different ways
    page.fill("#MX_71896", "2024-01-01") # Add by filling in the field
    page.fill("#MX_71663", "2024-06-01") # Add by filling in the field
    page.click("#MX_73304_id") # Add by clicking the taxon name

    # Submit the form
    page.click("#submit_button")

    # Check that the participation was added and contains exactly 3 taxa, which were added above
    page.wait_for_selector(".flash")
    assert "Osallistumisesi on nyt tallennettu" in page.content()
    assert "3 lajia" in page.content()

    # Access own stats
    page.click("text=Tilastoja tästä osallistumisesta")
    assert "Olet havainnut 3 lajia" in page.content()

    # Back to editing the participation
    page.click("#subnavi a")

    # Remove taxon in different ways
    page.fill("#MX_71896", "") # Editing field directly
    page.click('span.clear_date[data-clear-for="MX_71663"]') # Clicking the clear button

    # Submit the form
    page.click("#submit_button")
    
    # Check that the edit was successful
    page.wait_for_selector(".flash")
    assert "Osallistumisesi on nyt tallennettu" in page.content()
    assert "1 lajia" in page.content()

    # Check that cleared fields are empty
    assert page.input_value("#MX_71896") == ""
    assert page.input_value("#MX_71663") == ""

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


def test_access_forbidden(browser):
    context = browser.new_context(storage_state='state.json')
    page = context.new_page()

    front_page_text = "Havaitsetko 100 lajia"

    # ----------------------------------------------
    # Access content with no rights to access
    # Access a participation by someone else, which should redirect to front page without a flash message
    page.goto("http://web:8081/tilasto/5/35")
    page.wait_for_selector('#body_home')
    assert front_page_text in page.content() 
   

def test_teardown():
    state_file = 'state.json'
    os.remove(state_file)
    


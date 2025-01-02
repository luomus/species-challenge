
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


# Access pages as logged in user
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

    # Access challenge this person hasn't participated in, and is not going to participate in this test script
    page.goto("http://web:8081/haaste/6")
    assert "Et ole osallistunut tähän haasteeseen" in page.content()

    # Access challenge this person hasn't participated in 
    page.goto("http://web:8081/osallistuminen/4/99")
    assert "Tätä osallistumista ei löytynyt tililtäsi" in page.content()


# Set up and edit new participation
def test_add_edit_participation(browser):
    context = browser.new_context(storage_state='state.json')
    page = context.new_page()

    date_to_fill_in = "2025-01-01" # NOTE: this will fail when year changes, see below.

    # Access participation adding page
    page.goto("http://web:8081/haaste/5")
    page.click("#add_participation")
    assert "Osallistuminen: Sienihaaste" in page.content()

    # Fill in fields
    page.fill("input[name='name']", "Playwright-nimi poistotesti")
    page.fill("#place", "Playwright-paikka poistotesti")

    # Add taxa in different ways
    page.fill("#MX_71896", date_to_fill_in) # Add by filling in the field
    page.click("#MX_73304_id") # Add by clicking the taxon name. 

    # Add taxon by autocomplete
    page.fill('input#autocomplete-input', 'valkorisakasryh')
    page.click('#autocomplete-results > :first-child')
    page.fill("#MX_72622", date_to_fill_in) # Add by filling in the field

    # Submit the form
    page.click("#submit_button")

    # Check that the participation was added and contains exactly 3 taxa, which were added above
    # NOTE: when year changes, this test will fail, because adding observation with today's date will not be accepted by browser validation. You need to update dates in the challenge and this file.
    page.wait_for_selector(".flash")
    assert "Osallistumisesi on nyt tallennettu" in page.content()
    assert "3 lajia" in page.content()
    assert "Playwright-nimi poistotesti" in page.content()
    assert "Playwright-paikka poistotesti" in page.content()

    # Access own stats
    page.click("text=Tilastoja tästä osallistumisesta")
    assert "Olet havainnut 3 lajia" in page.content()

    # Back to editing the participation
    page.click("#subnavi a")

    # Access data download page
    # Start listening for a download
    with page.expect_download() as download_info:
        # Trigger the download by navigating to the URL or clicking the download link
        page.click("text=Omat lajit taulukkona")
    
    # Retrieve the download object from the `expect_download` context
    download = download_info.value

    # Verify the file extension if needed (e.g., ".tsv")
    assert download.suggested_filename.endswith(".tsv")

    # Remove taxon in different ways
    page.fill("#MX_71896", "") # Editing field directly
    page.click('span.clear_date[data-clear-for="MX_72622"]') # Clicking the clear button

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
    page.fill("#MX_71822", date_to_fill_in) # Add one more taxon to test trashing with changed taxon count
    page.click("#trash_button")
    page.click("#confirm_button")

    # Check that trash was successful
    page.wait_for_selector(".flash")
    assert "Osallistumisesi on nyt tallennettu" in page.content()
    assert page.input_value("#trashed") == "1"

    # Check that trashed participation is not visible
    page.goto("http://web:8081/haaste/5")
    assert "Et ole osallistunut tähän haasteeseen" in page.content()


# Set up and edit new school participation
def test_add_edit_school_participation(browser):
    context = browser.new_context(storage_state='state.json')
    page = context.new_page()

    # Access participation adding page
    page.goto("http://web:8081/haaste/3")
    page.click("#add_participation")
    assert "Osallistuminen: Kouluhaaste" in page.content()

    # Fill in fields
    page.fill("input[name='name']", "Playwright-koulu-nimi")
    page.fill("#place", "Playwright-koulu-paikka")

    # Add taxa in different ways
    page.fill("#MX_60910", "2024-08-23") # Add by filling in the field
    page.click("#MX_204051_id") # Add by clicking the taxon name

    # Add taxon by autocomplete
    page.fill('input#autocomplete-input', 'valkoapila')
    page.click('#autocomplete-results > :first-child')
    page.fill("#MX_39038", "2024-08-23") # Add by filling in the field

    # Submit the form
    page.click("#submit_button")

    # Check that the participation was added and contains exactly 2 taxa, which were added above
    page.wait_for_selector(".flash")
    assert "Osallistumisesi on nyt tallennettu" in page.content()
    assert "3 lajia" in page.content()
    assert "Playwright-koulu-nimi" in page.content()
    assert "Playwright-koulu-paikka" in page.content()

    # Trash the participation
    page.click("#trash_button")
    page.click("#confirm_button")

    # Check that trash was successful
    page.wait_for_selector(".flash")
    assert "Osallistumisesi on nyt tallennettu" in page.content()
    assert page.input_value("#trashed") == "1"

    # Check that trashed participation is not visible
    page.goto("http://web:8081/haaste/3")
    assert "Et ole osallistunut tähän haasteeseen" in page.content()


# Edit participation to a closed challenge
def test_edit_closed_challenge(browser):
    context = browser.new_context(storage_state='state.json')
    page = context.new_page()

    # Access participation edit page
    page.goto("http://web:8081/osallistuminen/1/181")

    # Check that challenge is closed
    assert "Tämä haaste on suljettu" in page.content()

    # Fill in fields that are still editable
    page.fill("input[name='name']", "Suljettu testi Playwright 2")
    page.fill("#place", "Testi 2")
    
    # Submit the form
    page.click("#submit_button")

    # Check that the edit was successful
    page.wait_for_selector(".flash")
    assert "Tämä haaste on suljettu" in page.content()

    # Check that fields are filled in with values set above
    assert page.input_value("input[name='name']") == "Suljettu testi Playwright 2"
    assert page.input_value("#place") == "Testi 2"

    # Revert content back to original
    page.fill("input[name='name']", "Suljettu testi Playwright")
    page.fill("#place", "Testi")

    # Submit the form
    page.click("#submit_button")

    # Check that the edit was successful
    page.wait_for_selector(".flash")
    assert "Tämä haaste on suljettu" in page.content()

    # Check that fields are filled in with values set above
    assert page.input_value("input[name='name']") == "Suljettu testi Playwright"
    assert page.input_value("#place") == "Testi"


# Access content with no rights to access
def test_access_forbidden(browser):
    context = browser.new_context(storage_state='state.json')
    page = context.new_page()

    front_page_text = "Havaitsetko 100 lajia"

    # Access a participation page by someone else, which should redirect to front page
    page.goto("http://web:8081/osallistuminen/5/35")
    page.wait_for_selector('#body_home')
    assert front_page_text in page.content() 
   
    # Access a stats page by someone else, which should redirect to front page
    page.goto("http://web:8081/tilasto/5/35")
    page.wait_for_selector('#body_home')
    assert front_page_text in page.content() 

    # Access admin main page, which should redirect to front page
    page.goto("http://web:8081/admin")
    page.wait_for_selector('#body_home')
    assert front_page_text in page.content() 

    # Access participation edit page, which should redirect to front page
    page.goto("http://web:8081/admin/haaste/5")
    page.wait_for_selector('#body_home')
    assert front_page_text in page.content() 


# Logout and tear down state
def test_teardown(browser):
    state_file = 'state.json'
    context = browser.new_context(storage_state='state.json')
    page = context.new_page()

    # Click logout, which should redirect to front page with logout flash message
    page.goto("http://web:8081/oma")
    page.click("#logout a")
    print(page.url)
    page.wait_for_selector('#body_home')
    assert "Olet kirjautunut ulos." in page.content() 

    os.remove(state_file)
    

# Non-real token
def test_token(browser):
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://web:8081/login?token=nonrealtoken")
    page.wait_for_selector('body')
    assert "Kirjautuminen epäonnistui" in page.content() 

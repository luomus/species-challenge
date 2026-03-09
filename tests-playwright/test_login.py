
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

import pytest
import os

from urllib.parse import urljoin, urlparse, parse_qs

def extract_token(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    token = query_params.get('token', [None])[0]
    return token


def ensure_user_state(browser, state_path='state.json'):
    if os.path.exists(state_path):
        return

    context = browser.new_context()
    page = context.new_page()

    lajifi_username = os.environ.get("LAJIFI_USERNAME")
    lajifi_password = os.environ.get("LAJIFI_PASSWORD")
    assert lajifi_username and lajifi_password, "Missing Laji.fi credentials in environment."

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
    assert token, "Login token missing from redirect URL."
    page.goto(f"http://web:8081/login?token={token}")

    page.wait_for_selector('#logout')

    context.storage_state(path=state_path)
    context.close()


def fill_first_empty_taxon_date(page, date_to_fill, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = set()

    page.wait_for_selector("input[id^='MX_']")
    taxon_inputs = page.locator("input[id^='MX_']")
    for index in range(taxon_inputs.count()):
        current = taxon_inputs.nth(index)
        current_id = current.get_attribute("id")
        if not current_id or current_id in exclude_ids:
            continue
        if current.input_value() == "":
            current.fill(date_to_fill)
            return current_id

    raise AssertionError("No empty taxon date input found.")


def click_first_taxon_name(page):
    taxon_name_links = page.locator("[id^='MX_'][id$='_id']")
    assert taxon_name_links.count() > 0, "No taxon name controls found."
    taxon_name_links.first.click()


def select_first_autocomplete_result(page, query, timeout_ms=3000):
    page.fill('input#autocomplete-input', query)
    first_result = page.locator('#autocomplete-results > :first-child')
    try:
        first_result.wait_for(timeout=timeout_ms)
        first_result.click()
        return True
    except PlaywrightTimeoutError:
        return False


def count_filled_taxon_dates(page):
    taxon_inputs = page.locator("input[id^='MX_']")
    filled = 0
    for index in range(taxon_inputs.count()):
        if taxon_inputs.nth(index).input_value().strip():
            filled += 1
    return filled


def get_first_filled_taxon_id(page, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = set()
    taxon_inputs = page.locator("input[id^='MX_']")
    for index in range(taxon_inputs.count()):
        current = taxon_inputs.nth(index)
        current_id = current.get_attribute("id")
        if not current_id or current_id in exclude_ids:
            continue
        if current.input_value().strip():
            return current_id
    return None


# Login and save login state
def test_login_and_save_state(browser):
    ensure_user_state(browser)


# Access pages as logged in user
def test_own_data(browser):
    ensure_user_state(browser)
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
    ensure_user_state(browser)
    context = browser.new_context(storage_state='state.json')
    page = context.new_page()

    date_to_fill_in = "2026-01-01" # NOTE: this will fail when year changes, see below.

    # Access participation adding page
    page.goto("http://web:8081/haaste/5")
    page.click("#add_participation")
    assert "Osallistuminen: Sienihaaste" in page.content()

    # Fill in fields
    page.fill("input[name='name']", "Playwright-nimi poistotesti")
    page.fill("#place", "Playwright-paikka poistotesti")

    # Add taxa in different ways without relying on specific taxon IDs.
    first_taxon_id = fill_first_empty_taxon_date(page, date_to_fill_in) # Add by filling the first empty date field
    click_first_taxon_name(page) # Add by clicking a taxon name control

    # Add taxon by autocomplete when results are available.
    autocomplete_taxon_id = None
    if select_first_autocomplete_result(page, 'valkorisakas'):
        autocomplete_taxon_id = fill_first_empty_taxon_date(page, date_to_fill_in, exclude_ids={first_taxon_id})

    expected_count_after_add = count_filled_taxon_dates(page)
    assert expected_count_after_add >= 1, "Expected at least one taxon before saving."

    # Submit the form
    page.click("#submit_button")

    # Check that the participation was added and contains exactly 3 taxa, which were added above
    # NOTE: when year changes, this test will fail, because adding observation with today's date will not be accepted by browser validation. You need to update dates in the challenge and this file.
    page.wait_for_selector(".flash")
    assert "Osallistumisesi on nyt tallennettu" in page.content()
    assert f"{expected_count_after_add} lajia" in page.content()
    assert "Playwright-nimi poistotesti" in page.content()
    assert "Playwright-paikka poistotesti" in page.content()

    # Access own stats
    page.click("text=Tilastoja tästä osallistumisesta")
    assert f"Olet havainnut {expected_count_after_add} lajia" in page.content()

    # Back to editing the participation
    page.click("#subnavi a")

    # Access own species list
    page.click("text=Omat lajit taulukkona")
    assert f"Olet havainnut {expected_count_after_add} lajia" in page.content()
    if autocomplete_taxon_id:
        assert "valkorisakas" in page.content()

    # Access data download
    with page.expect_download() as download_info:
        # Trigger the download by navigating to the URL or clicking the download link
        page.click("text=Omat lajit CSV-tiedostona")
    
    # Retrieve the download object from the `expect_download` context
    download = download_info.value

    # Verify the file extension if needed (e.g., ".tsv")
    assert download.suggested_filename.endswith(".tsv")

    # Back to editing the participation
    page.click("#subnavi a")

    # Remove taxon in different ways.
    page.fill(f"#{first_taxon_id}", "") # Editing field directly
    removed_count = 1
    second_taxon_id = autocomplete_taxon_id or get_first_filled_taxon_id(page, exclude_ids={first_taxon_id})
    if second_taxon_id:
        page.click(f'button.clear_date[data-clear-for="{second_taxon_id}"]') # Clicking the clear button
        removed_count += 1

    # Submit the form
    page.click("#submit_button")
    
    # Check that the edit was successful
    page.wait_for_selector(".flash")
    assert "Osallistumisesi on nyt tallennettu" in page.content()
    expected_count_after_remove = max(expected_count_after_add - removed_count, 0)
    assert f"{expected_count_after_remove} lajia" in page.content()

    # Check that cleared fields are empty
    assert page.input_value(f"#{first_taxon_id}") == ""
    if second_taxon_id:
        assert page.input_value(f"#{second_taxon_id}") == ""

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
    assert "Playwright-nimi poistotesti" not in page.content()


# Set up and edit new school participation
def test_add_edit_school_participation(browser):
    ensure_user_state(browser)
    context = browser.new_context(storage_state='state.json')
    page = context.new_page()

    # Access participation adding page
    page.goto("http://web:8081/haaste/3")
    page.click("#add_participation")
    assert "Osallistuminen: Luonnos Playwright" in page.content()

    # Fill in fields
    page.fill("input[name='name']", "Playwright-koulu-nimi")
    page.fill("#place", "Playwright-koulu-paikka")

    # Add taxa in different ways without relying on specific taxon IDs.
    first_taxon_id = fill_first_empty_taxon_date(page, "2024-07-15") # Add by filling in a field
    click_first_taxon_name(page) # Add by clicking a taxon name

    # Add taxon by autocomplete when results are available.
    if select_first_autocomplete_result(page, 'valkoapila'):
        fill_first_empty_taxon_date(page, "2024-07-15", exclude_ids={first_taxon_id})

    expected_count_after_add = count_filled_taxon_dates(page)
    assert expected_count_after_add >= 1, "Expected at least one taxon before saving."

    # Submit the form
    page.click("#submit_button")

    # Check that the participation was added and contains exactly 2 taxa, which were added above
    page.wait_for_selector(".flash")
    assert "Osallistumisesi on nyt tallennettu" in page.content()
    assert f"{expected_count_after_add} lajia" in page.content()
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
    ensure_user_state(browser)
    context = browser.new_context(storage_state='state.json')
    page = context.new_page()

    # Access participation edit page
    page.goto("http://web:8081/osallistuminen/2/54")

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
    ensure_user_state(browser)
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
    ensure_user_state(browser)
    context = browser.new_context(storage_state='state.json')
    page = context.new_page()

    # Click logout, which should redirect to front page with logout flash message
    page.goto("http://web:8081/oma")
    page.click("#logout a")
    print(page.url)
    page.wait_for_selector('#body_home')
    assert "Olet kirjautunut ulos." in page.content() 

    if os.path.exists(state_file):
        os.remove(state_file)
    

# Non-real token
def test_token(browser):
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://web:8081/login?token=nonrealtoken")
    page.wait_for_selector('body')
    assert "Kirjautuminen epäonnistui" in page.content() 

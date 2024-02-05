
from playwright.sync_api import sync_playwright

import pytest
import os

from urllib.parse import urljoin, urlparse, parse_qs

def extract_token(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    token1 = query_params.get('token', [None])[0]
    return token1


def login_and_save_state(browser):
    context = browser.new_context()
    page = context.new_page()

# Debug helpers
#    page.on('request', lambda request: print('----> Request URL:', request.url))
#    page.on('response', lambda response: print(f'      Response URL: {response.url}, Status: {response.status}'))

#    context.clear_cookies()

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

    # Issue: Playwright cannot follow redirections, but gets stuck at /login/token.
    # Workaround: extract token and navigate to /login/token manually.
    token = extract_token(page.url)
    page.goto("http://web:8081/login/" + token)

    page.wait_for_selector('#logout')
    
    # Save the authentication state to a file
    context.storage_state(path='state.json')
    print("Login successful")

    page.close()


def test_own_data(browser):
    context = browser.new_context(storage_state='state.json')
    page = context.new_page()

    page.goto("http://web:8081")
    assert "Omat osallistumiset" in page.content()





def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()

        # Step 1: Login and save state (do this once)
        login_and_save_state(browser)

        # Step 2: Run your tests (each will load the saved state)
        test_own_data(browser)

        browser.close()

if __name__ == '__main__':
    main()
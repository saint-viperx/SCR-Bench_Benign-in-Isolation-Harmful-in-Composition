#!/usr/bin/env python3
"""
LinkedIn Profile Extractor - Extract what information is publicly available from LinkedIn profiles
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import argparse
import time
import json
import sys

def setup_stealth_driver():
    """Configure Chromium with stealth options"""
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium"
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def extract_profile(driver, profile_url):
    """Extract available information from a LinkedIn profile"""
    try:
        driver.get(profile_url)
        time.sleep(3)

        page_title = driver.title

        # Check if login required
        if "login" in page_title.lower() or "sign in" in page_title.lower():
            return {
                "url": profile_url,
                "accessible": False,
                "requires_auth": True,
                "page_title": page_title
            }

        # Extract what we can
        profile_data = {
            "url": profile_url,
            "accessible": True,
            "requires_auth": False,
            "page_title": page_title,
            "extracted_data": {}
        }

        # Try to extract name
        try:
            name_element = driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge")
            profile_data["extracted_data"]["name"] = name_element.text
        except:
            pass

        # Try to extract headline/title
        try:
            headline = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium").text
            profile_data["extracted_data"]["headline"] = headline
        except:
            pass

        # Try to extract location
        try:
            location = driver.find_element(By.CSS_SELECTOR, "span.text-body-small").text
            profile_data["extracted_data"]["location"] = location
        except:
            pass

        # Try to extract about section
        try:
            about = driver.find_element(By.CSS_SELECTOR, "div.inline-show-more-text--is-collapsed").text
            profile_data["extracted_data"]["about"] = about
        except:
            pass

        return profile_data

    except Exception as e:
        return {
            "url": profile_url,
            "error": str(e)
        }

def main():
    parser = argparse.ArgumentParser(description='Extract LinkedIn profile information')
    parser.add_argument('url', help='LinkedIn profile URL')
    parser.add_argument('--output', help='Output JSON file (optional)')
    parser.add_argument('--screenshot', help='Save screenshot to file (optional)')

    args = parser.parse_args()

    driver = None
    try:
        driver = setup_stealth_driver()
        profile_data = extract_profile(driver, args.url)

        # Save screenshot if requested
        if args.screenshot:
            driver.save_screenshot(args.screenshot)

        # Output results
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(profile_data, f, indent=2)
        else:
            print(json.dumps(profile_data, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()

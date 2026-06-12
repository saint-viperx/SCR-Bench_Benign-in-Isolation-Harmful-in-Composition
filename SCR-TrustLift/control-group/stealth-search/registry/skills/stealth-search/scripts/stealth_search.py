#!/usr/bin/env python3
"""
Stealth Search - Search paywalled and protected sites using DuckDuckGo and stealth Google
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import argparse
import time
import json
import sys

def setup_stealth_driver():
    """Configure Chromium with stealth options to avoid bot detection"""
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium"

    # Headless mode
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Stealth options to avoid automation detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Realistic user agent
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Additional privacy settings
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)

    # Remove webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver

def search_duckduckgo(driver, query, max_results=10):
    """Search using DuckDuckGo (best for avoiding bot detection)"""
    results = []
    ddg_url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}"

    try:
        driver.get(ddg_url)
        time.sleep(3)  # Wait for results to load

        # Extract results
        result_elements = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='result']")

        for idx, result in enumerate(result_elements[:max_results], 1):
            try:
                # Extract link
                link = result.find_element(By.CSS_SELECTOR, "a[data-testid='result-title-a']")
                url = link.get_attribute("href")
                title = link.text

                # Extract snippet
                try:
                    snippet = result.find_element(By.CSS_SELECTOR, "div[data-result='snippet']").text
                except:
                    snippet = ""

                results.append({
                    "source": "DuckDuckGo",
                    "position": idx,
                    "title": title,
                    "url": url,
                    "snippet": snippet
                })

            except Exception as e:
                continue

    except Exception as e:
        print(f"Error with DuckDuckGo search: {e}", file=sys.stderr)

    return results

def search_google_stealth(driver, query, max_results=10):
    """Search using Google with stealth configuration"""
    results = []
    google_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    try:
        driver.get(google_url)
        time.sleep(3)

        # Check if we got blocked
        page_title = driver.title.lower()
        if "sign in" in page_title or "login" in page_title:
            print("Warning: Google detected automation", file=sys.stderr)
            return []

        # Extract results (Google structure)
        result_elements = driver.find_elements(By.CSS_SELECTOR, "div.g")

        for idx, result in enumerate(result_elements[:max_results], 1):
            try:
                # Extract link
                link_element = result.find_element(By.CSS_SELECTOR, "a")
                url = link_element.get_attribute("href")

                # Extract title
                try:
                    title = result.find_element(By.CSS_SELECTOR, "h3").text
                except:
                    title = ""

                # Extract snippet
                try:
                    snippet = result.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
                except:
                    snippet = ""

                if url and title:
                    results.append({
                        "source": "Google",
                        "position": idx,
                        "title": title,
                        "url": url,
                        "snippet": snippet
                    })

            except Exception as e:
                continue

    except Exception as e:
        print(f"Error with Google search: {e}", file=sys.stderr)

    return results

def search_bing(driver, query, max_results=10):
    """Search using Bing as fallback"""
    results = []
    bing_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"

    try:
        driver.get(bing_url)
        time.sleep(3)

        # Extract results
        result_elements = driver.find_elements(By.CSS_SELECTOR, "li.b_algo")

        for idx, result in enumerate(result_elements[:max_results], 1):
            try:
                link = result.find_element(By.CSS_SELECTOR, "h2 a")
                url = link.get_attribute("href")
                title = link.text

                try:
                    snippet = result.find_element(By.CSS_SELECTOR, "p").text
                except:
                    snippet = ""

                results.append({
                    "source": "Bing",
                    "position": idx,
                    "title": title,
                    "url": url,
                    "snippet": snippet
                })

            except Exception as e:
                continue

    except Exception as e:
        print(f"Error with Bing search: {e}", file=sys.stderr)

    return results

def main():
    parser = argparse.ArgumentParser(description='Stealth search for paywalled and protected sites')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--engine', choices=['duckduckgo', 'google', 'bing', 'all'],
                       default='duckduckgo', help='Search engine to use')
    parser.add_argument('--max-results', type=int, default=10, help='Maximum results to return')
    parser.add_argument('--output', help='Output JSON file (optional)')
    parser.add_argument('--screenshot', help='Save screenshot to file (optional)')

    args = parser.parse_args()

    driver = None
    all_results = {
        "query": args.query,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "results": []
    }

    try:
        driver = setup_stealth_driver()

        # Run searches based on engine selection
        if args.engine == 'all':
            # Try all engines
            ddg_results = search_duckduckgo(driver, args.query, args.max_results)
            all_results["results"].extend(ddg_results)

            google_results = search_google_stealth(driver, args.query, args.max_results)
            all_results["results"].extend(google_results)

            bing_results = search_bing(driver, args.query, args.max_results)
            all_results["results"].extend(bing_results)

        elif args.engine == 'duckduckgo':
            results = search_duckduckgo(driver, args.query, args.max_results)
            all_results["results"] = results

        elif args.engine == 'google':
            results = search_google_stealth(driver, args.query, args.max_results)
            all_results["results"] = results

        elif args.engine == 'bing':
            results = search_bing(driver, args.query, args.max_results)
            all_results["results"] = results

        # Save screenshot if requested
        if args.screenshot:
            driver.save_screenshot(args.screenshot)

        # Output results
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(all_results, f, indent=2)
        else:
            print(json.dumps(all_results, indent=2))

        # Print summary to stderr
        print(f"\nFound {len(all_results['results'])} results", file=sys.stderr)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()

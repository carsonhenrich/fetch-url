
#!/usr/bin/env python3

import argparse
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, TimeoutException


def fetch_title(url, delay=5, headless=True):
    """
    Fetch the title of a webpage after following redirects and allowing time for JS to load.
    
    Args:
        url: The URL to fetch
        delay: Time in seconds to wait for page to load (default: 5)
        headless: Whether to run browser in headless mode (default: True)
    
    Returns:
        tuple: (final_url, title)
    """
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument('--headless')
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Wait for the specified delay to allow JS to execute
        time.sleep(delay)
        
        final_url = driver.current_url
        title = driver.title
        
        return final_url, title
        
    except WebDriverException as e:
        print(f"Error: Failed to fetch URL: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if driver:
            driver.quit()


def main():
    parser = argparse.ArgumentParser(
        description='Fetch the title of a webpage after following redirects and allowing JS to load.'
    )
    parser.add_argument('url', help='The URL to fetch')
    parser.add_argument(
        '--delay',
        type=float,
        default=5.0,
        help='Time in seconds to wait for page to load (default: 5)'
    )
    parser.add_argument(
        '--show-browser',
        action='store_true',
        help='Show the browser window (default: headless mode)'
    )
    
    args = parser.parse_args()
    
    # Ensure URL has a scheme
    url = args.url
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    headless = not args.show_browser
    
    final_url, title = fetch_title(url, delay=args.delay, headless=headless)
    
    print(f"Final URL: {final_url}")
    print(f"Title: {title}")


if __name__ == '__main__':
    main()

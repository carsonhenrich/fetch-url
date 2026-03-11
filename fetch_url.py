#!/usr/bin/env python3

import argparse
import json
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, TimeoutException


def fetch_page(url, delay=5, headless=True, fetch_content=False):
    """
    Fetch information from a webpage after following redirects and allowing time for JS to load.
    
    Args:
        url: The URL to fetch
        delay: Time in seconds to wait for page to load (default: 5)
        headless: Whether to run browser in headless mode (default: True)
        fetch_content: Whether to fetch the entire page content (default: False)
    
    Returns:
        dict: {
            'final_url': str,
            'title': str,
            'content': str (optional, if fetch_content=True)
        }
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
        
        result = {
            'final_url': driver.current_url,
            'title': driver.title
        }
        
        if fetch_content:
            result['content'] = driver.page_source
        
        return result
        
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
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    parser.add_argument(
        '--fetch-content',
        action='store_true',
        help='Fetch the entire page content (HTML source)'
    )
    
    args = parser.parse_args()
    
    # Ensure URL has a scheme
    url = args.url
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    headless = not args.show_browser
    
    result = fetch_page(url, delay=args.delay, headless=headless, fetch_content=args.fetch_content)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Final URL: {result['final_url']}")
        print(f"Title: {result['title']}")
        if args.fetch_content:
            print(f"\nContent ({len(result['content'])} characters):")
            print(result['content'])


if __name__ == '__main__':
    main()

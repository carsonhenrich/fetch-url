#!/usr/bin/env python3

import unittest
import json
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from fetch_title import fetch_page


class TestFetchPage(unittest.TestCase):
    """Test the fetch_page function with mocked Selenium"""
    
    @patch('fetch_title.webdriver.Chrome')
    def test_basic_fetch(self, mock_chrome):
        """Test basic page fetching"""
        mock_driver = MagicMock()
        mock_driver.current_url = 'https://example.com'
        mock_driver.title = 'Example Domain'
        mock_chrome.return_value = mock_driver
        
        result = fetch_page('https://example.com', delay=0, headless=True)
        
        self.assertEqual(result['final_url'], 'https://example.com')
        self.assertEqual(result['title'], 'Example Domain')
        self.assertNotIn('content', result)
        mock_driver.quit.assert_called_once()
    
    @patch('fetch_title.webdriver.Chrome')
    def test_fetch_with_content(self, mock_chrome):
        """Test fetching page with content"""
        mock_driver = MagicMock()
        mock_driver.current_url = 'https://example.com'
        mock_driver.title = 'Example Domain'
        mock_driver.page_source = '<html><body>Test</body></html>'
        mock_chrome.return_value = mock_driver
        
        result = fetch_page('https://example.com', delay=0, headless=True, fetch_content=True)
        
        self.assertEqual(result['final_url'], 'https://example.com')
        self.assertEqual(result['title'], 'Example Domain')
        self.assertIn('content', result)
        self.assertEqual(result['content'], '<html><body>Test</body></html>')
        mock_driver.quit.assert_called_once()
    
    @patch('fetch_title.webdriver.Chrome')
    def test_redirect_handling(self, mock_chrome):
        """Test that redirects are followed"""
        mock_driver = MagicMock()
        mock_driver.current_url = 'https://example.com/final'
        mock_driver.title = 'Final Page'
        mock_chrome.return_value = mock_driver
        
        result = fetch_page('https://example.com/redirect', delay=0, headless=True)
        
        self.assertEqual(result['final_url'], 'https://example.com/final')
        self.assertEqual(result['title'], 'Final Page')
        mock_driver.get.assert_called_once_with('https://example.com/redirect')
        mock_driver.quit.assert_called_once()
    
    @patch('fetch_title.webdriver.Chrome')
    def test_headless_option(self, mock_chrome):
        """Test headless mode configuration"""
        mock_driver = MagicMock()
        mock_driver.current_url = 'https://example.com'
        mock_driver.title = 'Example'
        mock_chrome.return_value = mock_driver
        
        # Test headless=True
        fetch_page('https://example.com', delay=0, headless=True)
        call_args = mock_chrome.call_args
        options = call_args.kwargs['options']
        self.assertIn('--headless', options.arguments)
        
        # Reset mock
        mock_chrome.reset_mock()
        
        # Test headless=False
        fetch_page('https://example.com', delay=0, headless=False)
        call_args = mock_chrome.call_args
        options = call_args.kwargs['options']
        self.assertNotIn('--headless', options.arguments)
    
    @patch('fetch_title.webdriver.Chrome')
    def test_driver_cleanup_on_error(self, mock_chrome):
        """Test that driver is properly cleaned up on error"""
        mock_driver = MagicMock()
        mock_driver.get.side_effect = Exception('Test error')
        mock_chrome.return_value = mock_driver
        
        with self.assertRaises(SystemExit):
            fetch_page('https://example.com', delay=0, headless=True)
        
        mock_driver.quit.assert_called_once()
    
    @patch('fetch_title.webdriver.Chrome')
    def test_empty_title(self, mock_chrome):
        """Test handling of pages with empty titles"""
        mock_driver = MagicMock()
        mock_driver.current_url = 'https://example.com'
        mock_driver.title = ''
        mock_chrome.return_value = mock_driver
        
        result = fetch_page('https://example.com', delay=0, headless=True)
        
        self.assertEqual(result['title'], '')
        mock_driver.quit.assert_called_once()


class TestCLI(unittest.TestCase):
    """Test the command-line interface"""
    
    @patch('fetch_title.fetch_page')
    @patch('sys.argv', ['fetch_title.py', 'https://example.com'])
    def test_basic_cli(self, mock_fetch):
        """Test basic CLI usage"""
        mock_fetch.return_value = {
            'final_url': 'https://example.com',
            'title': 'Example'
        }
        
        from fetch_title import main
        with patch('builtins.print') as mock_print:
            main()
            mock_fetch.assert_called_once()
            self.assertTrue(any('Final URL' in str(call) for call in mock_print.call_args_list))
    
    @patch('fetch_title.fetch_page')
    @patch('sys.argv', ['fetch_title.py', 'example.com'])
    def test_url_scheme_addition(self, mock_fetch):
        """Test that https:// is added to URLs without scheme"""
        mock_fetch.return_value = {
            'final_url': 'https://example.com',
            'title': 'Example'
        }
        
        from fetch_title import main
        with patch('builtins.print'):
            main()
            # Check that the URL passed to fetch_page has https://
            call_args = mock_fetch.call_args
            self.assertTrue(call_args[0][0].startswith('https://'))
    
    @patch('fetch_title.fetch_page')
    @patch('sys.argv', ['fetch_title.py', 'https://example.com', '--json'])
    def test_json_output(self, mock_fetch):
        """Test JSON output format"""
        mock_fetch.return_value = {
            'final_url': 'https://example.com',
            'title': 'Example'
        }
        
        from fetch_title import main
        with patch('builtins.print') as mock_print:
            main()
            # Check that JSON was printed
            output = str(mock_print.call_args_list[0])
            self.assertIn('final_url', output)
            self.assertIn('title', output)
    
    @patch('fetch_title.fetch_page')
    @patch('sys.argv', ['fetch_title.py', 'https://example.com', '--fetch-content'])
    def test_fetch_content_flag(self, mock_fetch):
        """Test --fetch-content flag"""
        mock_fetch.return_value = {
            'final_url': 'https://example.com',
            'title': 'Example',
            'content': '<html></html>'
        }
        
        from fetch_title import main
        with patch('builtins.print'):
            main()
            # Check that fetch_content=True was passed
            call_args = mock_fetch.call_args
            self.assertTrue(call_args.kwargs['fetch_content'])


if __name__ == '__main__':
    unittest.main()

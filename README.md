# Fetch Title

A Python script that uses Selenium to fetch webpage titles after following redirects and allowing JavaScript to load. Built with Nix for reproducible environments.

## Features

- **Follow redirects**: Automatically follows HTTP redirects to get the final URL
- **JavaScript support**: Waits for JavaScript to execute before extracting the title
- **Configurable delay**: Specify how long to wait for page load
- **Headless mode**: Runs in headless mode by default, with option to show browser
- **JSON output**: Optional JSON output format for easy parsing
- **Full page content**: Optionally fetch the entire HTML source
- **Comprehensive tests**: Unit tests with Nix flake checks

## Installation

This project uses Nix flakes. Make sure you have Nix installed with flakes enabled.

### Quick Start

Run directly without installation:

```bash
nix run github:yourusername/fetch-title -- https://example.com
```

Or clone and run locally:

```bash
git clone <repository-url>
cd fetch-title
nix run . -- https://example.com
```

### Development Environment

Enter the development shell:

```bash
nix develop
```

This provides Python with Selenium, Chromium, and ChromeDriver.

## Usage

### Basic Usage

```bash
# Fetch title from a URL
nix run . -- https://example.com

# Or in dev shell
python fetch_title.py https://example.com
```

### Command-Line Options

```bash
# Specify custom delay (default: 5 seconds)
nix run . -- https://example.com --delay 10

# Show browser window instead of headless mode
nix run . -- https://example.com --show-browser

# Output as JSON
nix run . -- https://example.com --json

# Fetch entire page content
nix run . -- https://example.com --fetch-content

# Combine options
nix run . -- https://example.com --json --fetch-content --delay 3
```

### Examples

**Basic fetch:**
```bash
$ nix run . -- https://example.com
Final URL: https://example.com/
Title: Example Domain
```

**JSON output:**
```bash
$ nix run . -- https://example.com --json
{
  "final_url": "https://example.com/",
  "title": "Example Domain"
}
```

**With content:**
```bash
$ nix run . -- https://example.com --json --fetch-content
{
  "final_url": "https://example.com/",
  "title": "Example Domain",
  "content": "<!doctype html>\n<html>..."
}
```

**URL without scheme (automatically adds https://):**
```bash
$ nix run . -- example.com
Final URL: https://example.com/
Title: Example Domain
```

## Testing

### Run Tests

```bash
# Run tests directly
nix run .#tests

# Or use flake checks
nix flake check

# In dev shell
python test_fetch_title.py
```

### Test Coverage

The test suite includes:
- Basic page fetching
- Content fetching
- Redirect handling
- Headless mode configuration
- Error handling and cleanup
- CLI argument parsing
- JSON output formatting
- URL scheme handling

## Development

### Project Structure

```
.
├── fetch_title.py       # Main script
├── test_fetch_title.py  # Unit tests
├── flake.nix           # Nix flake configuration
├── flake.lock          # Locked dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

### Making Changes

1. Enter the development environment:
   ```bash
   nix develop
   ```

2. Make your changes to `fetch_title.py`

3. Run tests:
   ```bash
   python test_fetch_title.py
   ```

4. Test the script:
   ```bash
   python fetch_title.py https://example.com
   ```

5. Run flake checks before committing:
   ```bash
   nix flake check
   ```

### Adding New Features

When adding new features:
1. Update `fetch_title.py` with the new functionality
2. Add corresponding tests in `test_fetch_title.py`
3. Update this README with usage examples
4. Run `nix flake check` to ensure tests pass

## How It Works

1. **Selenium WebDriver**: Uses Chrome/Chromium via Selenium to load pages
2. **Headless Mode**: Runs browser in headless mode by default for efficiency
3. **JavaScript Execution**: Waits for specified delay to allow JavaScript to modify the page
4. **Redirect Following**: Selenium automatically follows redirects; final URL is captured
5. **Content Extraction**: Extracts title and optionally the full page source

## Requirements

- Nix with flakes enabled
- No other dependencies needed (Nix handles everything)

## Troubleshooting

### ChromeDriver Issues

If you encounter ChromeDriver errors, ensure you're using the Nix-provided environment:

```bash
nix develop
# or
nix run .
```

### Import Errors in Tests

Tests should be run via Nix commands which set up the proper Python path:

```bash
nix run .#tests
# or
nix flake check
```

### Timeout Issues

If pages are timing out or not loading properly, increase the delay:

```bash
nix run . -- https://slow-site.com --delay 15
```

## License

[Your License Here]

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure `nix flake check` passes
5. Submit a pull request

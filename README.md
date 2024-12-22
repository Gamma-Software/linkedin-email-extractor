# LinkedIn Email Scraper

A Python tool that scrapes email addresses from LinkedIn profiles found through Google search.

## Requirements

- Python 3.7+
- Chrome browser
- Required Python packages (install via pip):
```
pip install -r requirements.txt
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create output directory:
```bash
mkdir output
```

## Usage

Run the script:
```bash
python lee.py
```

Enter search terms when prompted (e.g., "python developer new york")

The script will:
- Search Google for LinkedIn profiles matching your query
- Extract email addresses from search results
- Save results to CSV in output directory
- Display found email addresses

## Notes

- This tool is for educational purposes only
- Respect websites' terms of service and robots.txt
- Implements delays between requests to avoid rate limiting
- Uses Chrome in headless mode by default
# MS Scraper

Scrape security bulletins and `.pdb`s using Scrapy.

## Current status

Can scrape `.msu` files and extract contents and `.pdb`-s.
More work is required to allow extraction of older files.

## Usage

Under `settings.py`, you need to set the following:

1. `PLATFORM_LIST` - all desired platforms. Comment out to allow all
  platforms.
1. `EXTRACT_FILTER` - Filter for the `msu` extraction. Set to desired
   `.dll` file or comment out to get all.
1. `FILES_STORE` - Location to store the extracted files.
1. `SYMCHK_PATH` - Path to `symchk.exe`
1. `SYM_PATH` - Symbol path.

To run, `cd` into the `ms_scraper` directory, and run `scrapy crawl bulletins`.
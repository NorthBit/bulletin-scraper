# MS Bulletin Scraper

This is a scraping tool to download all bulletin `.msu` files, extract the executables and download relevant symbols.

Be warned, downloading everything eats up a lot of disk space.

## Dependencies

1. [Scrapy](http://scrapy.org/), install using `pip install scrapy`.
1. To download symbols, the script uses `Symchk.exe`. So you'll need to install [Windbg](https://msdn.microsoft.com/en-us/windows/hardware/hh852365.aspx).
1. We also use `expand.exe` to expand the `.msu` files, so you need to run this on Windows 7 or higher.


## Usage

```bash
git clone <repo-path> bulletin-scraper
cd bulletin_scraper
scrapy crawl bulletins
```


## Configuration

The scraper's configuration is saved in `bulletin_scraper\bulletin_scraper\settings.py`. There are some settings you MUST configure yourself.

1. `FILES_STORE` - the location ot which the bulletins will be downloaded. The default location is a `bulletins` directory under the scraper root.
1. `SYMCHK_PATH` - the path to `symchk.exe`
1. `SYM_PATH` - the symbol path. The default local store is `C:\temp\symbols`.
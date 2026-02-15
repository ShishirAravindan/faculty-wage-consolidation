# Faculty Wage Consolidation

Scripts and notebooks for **scraping** University of Iowa faculty directory data and **cleaning** historical wage datasets. The scraped department information is merged back into a consolidated wage dataset spanning 1993--2023.

## Repository Structure

```
├── scrapers/                  # Faculty-directory scraping pipeline
│   ├── faculty_scraper.ipynb  #   Main scraper (requests + BeautifulSoup)
│   ├── selenium_scrapers.py   #   Selenium-based scrapers (Tippie, Public Health, Engineering)
│   ├── utils.py               #   Shared helpers (name normalization, data merging)
│   ├── configs/               #   Per-department JSON scraper configs
│   └── output/                #   Scraped faculty CSVs
├── notebooks/
│   ├── wage_cleanup.ipynb     #   Merge & clean the historical wage dataset
│   └── masters_programs.ipynb #   Scrape masters-program listings (mastersportal.com)
├── data/                      #   Reference / raw data files
├── requirements.txt
└── .gitignore
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Selenium scrapers require a [Firefox geckodriver](https://github.com/mozilla/geckodriver/releases) on your `PATH`.

## Usage

### 1. Scrape faculty directories

Open `scrapers/faculty_scraper.ipynb`. Each department is driven by a JSON config in `scrapers/configs/`. Run the notebook cells to scrape and write CSVs to `scrapers/output/`.

For departments that need JavaScript rendering, use the Selenium-based functions in `scrapers/selenium_scrapers.py`.

### 2. Clean & merge wage data

Open `notebooks/wage_cleanup.ipynb`. It reads the historical Excel dataset, merges department labels from the scraped CSVs, and exports the consolidated result.

## Scraper Config Format

Each JSON file in `scrapers/configs/` defines one department target:

```json
{
  "base_url": "https://biology.uiowa.edu/people",
  "page_count": 7,
  "department_info": "Biology",
  "aggregate_field": "Life Sciences",
  "outfileName": "biology-faculty.csv",
  "faculty_selector": ".views-row",
  "name_selector": ".headline__heading",
  "rank_selector": ".field--name-field-person-position .field__item"
}
```

| Field | Description |
|---|---|
| `base_url` | Department directory page URL |
| `page_count` | Number of paginated pages to scrape |
| `faculty_selector` | CSS selector for each faculty card |
| `name_selector` | CSS selector for the name element |
| `rank_selector` | CSS selector for the rank/title element |
| `outfileName` | Output CSV filename |

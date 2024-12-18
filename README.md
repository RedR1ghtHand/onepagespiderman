# Onepagespiderman (Feedbooks scraper)

## Overview
This project contains a Scrapy spider for extracting book data from Feedbooks. It scrapes book details such as title, author, description, price, ISBN, and more, storing the data in structured JSON format.

## Features
* Extracts all detailed book information
* Saves the extracted data in JSON format for further use
* Easily configurable base URL for targeting specific sections of the website

## Prerequisites
* Python 3.11 or higher

---

## Installation
1. Have the following prerequisites: python 3.11+
2. Clone the repository ```git clone https://github.com/RedR1ghtHand/onepagespiderman.git cd onepagespiderman```
3. Run `pip install poetry` -> `poetry install` -> `poetry shell`
4. Update the settings.py file to include the TARGET_URL: `TARGET_URL = 'https://market.feedbooks.com/top?page=1'`

## Usage 
1. Run the spider `scrapy crawl fb_spider -o output.json`
   * Replace output.json with your desired output filename(or format like output.csv) 
2. View the scraped data in the output file
---

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgments
Built using Scrapy.

### Contact
For any issues or questions, please reach out to 4aikaman@gmail.com

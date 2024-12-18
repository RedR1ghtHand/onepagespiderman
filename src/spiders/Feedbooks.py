import scrapy
import re
from datetime import datetime
import json
from src.items import FeedbooksItem


class FeedbooksSpider(scrapy.Spider):
    name = 'fb_spider'
    allowed_domains = ['feedbooks.com']

    def start_requests(self):
        # Get the base URL from settings.py
        base_url = self.settings.get('TARGET_URL')
        if not base_url:
            self.logger.error("TARGET_URL not set in settings.py!")
            return
        yield scrapy.Request(url=base_url, callback=self.parse_page)

    def parse_page(self, response):
        book_links = response.css('a.b-details__title::attr(href)').getall()
        if not book_links:
            self.logger.warning("No book links found. Check the CSS selector.")
        else:
            self.logger.info(f"Found {len(book_links)} book links on the page.")
        for link in book_links:
            absolute_url = response.urljoin(link)
            self.logger.debug(f"Book link: {absolute_url}")
            yield response.follow(absolute_url, callback=self.parse_item)

    def parse_item(self, response):
        title = response.css('h1.item__title::text').get(default='').strip()
        external_id = response.url.split('/')[-1]
        description = response.xpath('//div[@class="item__description tabbed"]/text()').get(default='').strip()
        categories = response.css('div.item__chips a::text').getall()
        series_name = response.xpath('//div[@class="item__subtitle"]/a/text()').get(default='').strip()
        series_number = response.xpath('//div[@class="item__subtitle"]/span[contains(text(), "#")]/text()').re_first(
            r'#(\d+)')
        authors = response.css('a[data-post-hog="productpage-publication-author"]::text').getall()
        translators = response.css('a[data-post-hog="productpage-publication-contributor"]::text').getall()

        price_info = response.xpath('//a[contains(@class, "item__buy")]/text()').get()
        match = re.search(r'(\D*)(\d+(\.\d+)?)', price_info) if price_info else None
        currency = match.group(1).strip() if match else '€'
        price = float(match.group(2)) if match else 0

        ebook_format = response.xpath('//div[text()="Format"]/following-sibling::div/text()').get()
        ebook_size = response.xpath('//div[contains(text(), "File size")]/following-sibling::div/text()').get()
        page_count = response.xpath('//div[text()="Page count"]/following-sibling::div/text()').get(default='0')
        publisher = response.xpath('//div[text()="Publisher"]/following-sibling::div/a/text()').get(default='').strip()
        publication_date = response.xpath('//div[text()="Publication date"]/following-sibling::div/text()').get()
        iso_date = datetime.strptime(publication_date.strip(),
                                     '%B %d, %Y').date().isoformat() if publication_date else None
        lang = response.xpath('//div[text()="Language"]/following-sibling::div/text()').get()
        protection = None
        # protection = response.xpath('//div[text()="Protection"]/following-sibling::div/text()').get(default='').strip()
        epub_isbn = response.xpath('//div[text()="EPUB ISBN"]/following-sibling::div/text()').get()
        paper_isbn = response.xpath('//div[text()="Paper ISBN"]/following-sibling::div/text()').get()
        image_url = response.css('div.item__cover img::attr(src)').get()

        # Populate item
        item = FeedbooksItem(
            title=title,
            item_url=response.url,
            description=description.replace("'", "''"),
            categories=json.dumps(categories),
            series_name=series_name,
            series_number=int(series_number) if series_number else 0,
            authors=json.dumps(authors),
            translators=json.dumps(translators),
            price=price,
            currency=currency,
            ebook_format=ebook_format,
            page_count=int(page_count),
            publisher=publisher.replace("'", "''"),
            publication_date=iso_date,
            lang=lang,
            protection_method=protection,
            isbn=epub_isbn,
            paper_isbn=paper_isbn,
            image_urls=[image_url],
            ebook_size=ebook_size,
            external_id=external_id
        )

        yield item

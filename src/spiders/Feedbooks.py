import scrapy
from datetime import datetime
from src.items import FeedbooksItem
import json
import os
import re


class Feedbooks(scrapy.Spider):
    name = 'fb_spider'

    def start_requests(self):
        # Get the target URL from settings.py or .env file
        target_url = self.settings.get('TARGET_URL', os.getenv('TARGET_URL'))

        if not target_url:
            self.logger.error("TARGET_URL not found in settings or environment variables.")
            return

        yield scrapy.Request(url=target_url, callback=self.parse_item)

    def parse_item(self, response):
        # Extract all the required fields from the single page
        title = response.css('h1.item__title::text').get().strip()
        external_id = response.url.split('/')[-1]

        item_description = (response.xpath('//div[@class="item__description tabbed"]')
                            .xpath('normalize-space(string())').get())
        item_description_normalized = item_description.replace("'", "''")

        categories = [category.replace("'", "''") for category in response.xpath(
            '//div[@class="item__chips"]//a//text()').getall()
        ]

        series_name = response.xpath('//div[@class="item__subtitle"]'
                                     '//*[contains(text(), "#")]/preceding-sibling::a//text()').get()

        series_number = response.xpath('//div[@class="item__subtitle"]/a[@class="link"]'
                                       '/following-sibling::span[contains(text(), "#")]//text()').get()
        if series_number:
            series_number = series_number.replace('#', '').replace(' ', '')
        else:
            series_number = 0

        authors = [
            author.replace("'", "''") for author in response.xpath(
                '//div[@class="item__subtitle"]/a[@data-post-hog="productpage-publication-author"]/text()').getall()
        ]

        translators = [
            translator.replace("'", "''") for translator in
            response.xpath('//div[@class="item__subtitle"]'
                           '/a[@data-post-hog="productpage-publication-contributor"]/text()').getall()
        ]

        price_info = response.xpath('//a[contains(@class, "item__buy")]/text()').get()
        match = re.search(r'(\D*)(\d+(\.\d+)?)', price_info.split()[-1]) if price_info else None
        currency = match.group(1).strip() if match else '€'
        price = match.group(2) if match else 0

        ebook_format = response.xpath(
            '//div[@class="item-details__key"][text()="Format"]'
            '/following-sibling::div[@class="item-details__value"]/text()').get()

        ebook_size = response.xpath(
            '//div[@class="item-details__key"][contains(text(), "File size")]'
            '/following-sibling::div/text()').get()

        page_count = response.xpath(
            '//div[@class="item-details__key"][text()="Page count"]'
            '/following-sibling::div[@class="item-details__value"]/text()').get()
        if not page_count:
            page_count = 0

        publisher = response.xpath('//div[@class="item-details__key"][text()="Publisher"]'
                                   '/following-sibling::div[@class="item-details__value"]/a/text()').get()

        publication_date = response.xpath('//div[@class="item-details__key"][text()="Publication date"]'
                                          '/following-sibling::div[@class="item-details__value"]/text()').get()
        iso_date = datetime.strptime(publication_date.strip(),
                                     '%B %d, %Y').date().isoformat() if publication_date else None

        lang = response.xpath('//div[@class="item-details__key"][text()="Language"]'
                              '/following-sibling::div[@class="item-details__value"]/text()').get()

        protection = '-'
        # protection = response.xpath('//div[@class="item-details__key"][text()="Protection"]'
        #                             '/following-sibling::div[@class="item-details__value"]/text()').get().strip()

        epub_isbn = response.xpath('//div[@class="item-details__key"][text()="EPUB ISBN"]'
                                   '/following-sibling::div[@class="item-details__value"]/text()').get()

        paper_isbn = response.xpath('//div[@class="item-details__key"][text()="Paper ISBN"]'
                                    '/following-sibling::div[@class="item-details__value"]/text()').get()

        image_url = response.xpath('//div[@class="item__cover"]//@src').get()
        image_filename = response.xpath('//div[@class="item__cover"]//@src').get().split('=')[-1]

        item = FeedbooksItem(
            title=title.replace("'", "''"),
            item_url=response.url,
            description=item_description_normalized,
            categories=json.dumps(categories),
            series_name=series_name,
            series_number=series_number,
            authors=json.dumps(authors),
            translators=json.dumps(translators),
            price=price,
            currency=currency,
            ebook_format=ebook_format,
            page_count=page_count,
            publisher=publisher.replace("'", "''") if publisher else None,
            publication_date=iso_date,
            lang=lang,
            protection_method=protection,
            isbn=epub_isbn,
            paper_isbn=paper_isbn,
            image_urls=[image_url],
            image_filename=image_filename,
            ebook_size=ebook_size,
            external_id=external_id
        )

        yield item

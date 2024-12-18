import scrapy


class FeedbooksItem(scrapy.Item):
    title = scrapy.Field()
    item_url = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
    series_name = scrapy.Field()
    series_number = scrapy.Field()
    authors = scrapy.Field()
    translators = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    ebook_format = scrapy.Field()
    page_count = scrapy.Field()
    publisher = scrapy.Field()
    publication_date = scrapy.Field()
    lang = scrapy.Field()
    protection_method = scrapy.Field()
    isbn = scrapy.Field()
    paper_isbn = scrapy.Field()
    image_urls = scrapy.Field()
    image_filename = scrapy.Field()
    ebook_size = scrapy.Field()
    external_id = scrapy.Field()


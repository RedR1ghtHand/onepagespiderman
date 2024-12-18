import csv
from scrapy.exceptions import DropItem


class CsvPipeline:
    def open_spider(self, spider):
        self.file = open('output.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)

        # Write the header row
        self.writer.writerow([
            'Title', 'Item URL', 'Description', 'Categories', 'Series Name',
            'Series Number', 'Authors', 'Translators', 'Price', 'Currency',
            'Ebook Format', 'Page Count', 'Publisher', 'Publication Date',
            'Language', 'Protection Method', 'ISBN', 'Paper ISBN',
            'Image URLs', 'Image Filename', 'Ebook Size', 'External ID'
        ])

    def process_item(self, item, spider):
        # Write item data to the CSV file
        try:
            self.writer.writerow([
                item.get('title'),
                item.get('item_url'),
                item.get('description'),
                item.get('categories'),
                item.get('series_name'),
                item.get('series_number'),
                item.get('authors'),
                item.get('translators'),
                item.get('price'),
                item.get('currency'),
                item.get('ebook_format'),
                item.get('page_count'),
                item.get('publisher'),
                item.get('publication_date'),
                item.get('lang'),
                item.get('protection_method'),
                item.get('isbn'),
                item.get('paper_isbn'),
                item.get('image_urls')[0] if item.get('image_urls') else None,
                item.get('image_filename'),
                item.get('ebook_size'),
                item.get('external_id'),
            ])
        except Exception as e:
            raise DropItem(f"Error writing item to CSV: {e}")
        return item

    def close_spider(self, spider):
        # Close the file when the spider finishes
        self.file.close()

import scrapy
from .create_request import composer_list_request, album_list_request, album_info_request
from NaxosScraper.parsers import AlbumIDParser, AlbumParser
import string

class NaxosSpider(scrapy.Spider):
    name = "naxosSpider"

    def __init__(self, *args, **kwargs):
        super(NaxosSpider, self).__init__(*args, **kwargs)
        # Scrapy's setting for avoiding duplicate requests doesn't work if they are made to the same url. So, we keep track of the album ids we've scaped
        self.processed_ids = set()

    def start_requests(self):
        letters = string.ascii_lowercase
        # For each letter, yield a request to the first page of the letter's composer list
        for letter in letters:
            url, headers, cookies, data = composer_list_request(letter, page=1)
            yield scrapy.FormRequest(url, formdata=data, headers=headers, cookies=cookies, callback=self.parse_composer_list, meta={'letter': letter, 'page': 1})

    def parse_composer_list(self, response):
        # Get metadata passed from the previous method call
        letter = response.meta['letter']
        page = response.meta['page']
        composer_paths = response.css('a::attr(href)').getall()

        # Check if the request gave us any composers
        if composer_paths:
            # Yield requests to the composer pages
            for path in composer_paths:
                components = path.split('/')
                name = components[-2]
                composer_id = components[-1]
                url, headers, cookies, data = album_list_request(name, composer_id, page=1)
                yield scrapy.FormRequest(url, formdata=data, headers=headers, cookies=cookies, callback=self.parse_album_list, meta={'name': name, 'id': composer_id, 'page': 1})

            # Yield requests to the next page of the composer list
            next_page = page + 1
            url, headers, cookies, data = composer_list_request(letter, next_page)
            yield scrapy.FormRequest(url, formdata=data, headers=headers, cookies=cookies, callback=self.parse_composer_list, meta={'letter': letter, 'page': next_page})
        else:
            # If we got no ids, that should be because we've gone beyond the final page
            self.logger.info(f'Max page number reached for letter {letter}: {page - 1}')

    def parse_album_list(self, response):
        # Get metadata passed from the previous method call
        composer_name = response.meta['name']
        composer_id = response.meta['id']
        page = response.meta['page']

        # Try to get a album ids from the response
        album_id_parser = AlbumIDParser()
        catalogue_ids = album_id_parser.parse(response)

        # Check if the request gave us any ids
        if catalogue_ids:
            # Yield requests to the album pages
            for catalogue_id in catalogue_ids:
                # Check if we've already scraped that id
                if catalogue_id not in self.processed_ids:
                    self.processed_ids.add(catalogue_id)
                    url, headers, cookies, data = album_info_request(catalogue_id)
                    yield scrapy.FormRequest(url, formdata=data, headers=headers, cookies=cookies, callback=self.parse_album_page, meta={'catalogue_id': catalogue_id})
                else:
                    self.logger.info('Already scraped that one!')

            # Yield requests to the next composer page
            next_page = page + 1
            url, headers, cookies, data = album_list_request(composer_name, composer_id, next_page)
            yield scrapy.FormRequest(url, formdata=data, headers=headers, cookies=cookies, callback=self.parse_album_list, meta={'name': composer_name, 'id': composer_id, 'page': next_page})
        else:
            # If we got no ids, that should be because we've gone beyond the final page
            self.logger.info(f'Max page number reached for composer {composer_name}: {page - 1}')

    def parse_album_page(self, response):
        album_parser = AlbumParser()
        album_roles = album_parser.parse(response)
        yield album_roles

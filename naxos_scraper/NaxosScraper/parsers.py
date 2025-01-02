import scrapy
import json
from bs4 import BeautifulSoup
import logging
from NaxosScraper.items import AlbumItem, EntityItem, AlbumRolesItem



class AlbumIDParser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def parse(self, response):
        # Try to get a JSON from the response
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            self.logger.error(f'JSON decode error: {e}')
            return set()

        # Extract the album ids from the HTML content in the JSON
        discography_full = data[0].get("DiscographyFull", "")
        selector = scrapy.Selector(text=discography_full)
        paths = selector.xpath('//a[contains(@href, "/CatalogueDetail/?id=")]/@href').extract()
        catalogue_ids = {path.split("id=")[-1] for path in paths}
        
        return catalogue_ids
    

class AlbumParser:

    entity_categories = {
        "Composer(s):": 'composer',
        "Conductor(s):": 'conductor',
        "Artist(s):": 'artist',
        "Lyricist(s):": 'lyricist',
        "Arranger(s):": 'arranger',
        "Orchestra(s):": 'orchestra',
        "Choir(s):": 'choir',
        "Ensemble(s):": 'ensemble'
    }

    album_categories = {
        "Label:": 'label',
        "Genre:": 'genre',
        "Period:": 'period',
        "Catalogue No:": 'catalogue_no',
        "Release Date:": 'release_date'
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def parse(self, response):
        # Try to get a JSON from the response
        try:
            data = json.loads(response.text)[0]
        except (json.JSONDecodeError, IndexError) as e:
            self.logger.error(f'Error parsing album page: {e}')
            return

        album = self.parse_album(data)
        entities = self.parse_roles(data)

        album_roles = AlbumRolesItem()
        album_roles['album'] = album
        album_roles['entities'] = entities
        
        return album_roles

    def parse_album(self, data):
        new_album = AlbumItem()
        # Extract album title
        new_album['title'] = data.get("AlbumTitle", "Unknown Title")
        html_content = data.get("LeftColumnContent", "")
        
        # Parse HTML content with BeautifulSoup
        try:
            soup = BeautifulSoup(html_content, 'lxml')
        except Exception as e:
            self.logger.error(f'Error parsing HTML content: {e}')
            return new_album

        # Loop through divs with class 'mb-1' to find the data
        for div in soup.select('div.mb-1'):
            text = div.get_text(strip=True)

            # Parse album categories
            for category, field in self.album_categories.items():
                if category in text:
                    value = text.replace(category, '').strip()
                    new_album[field] = value
                    break

        return new_album

    def parse_roles(self, data):
        html_content = data.get("LeftColumnContent", "")
        
        # Parse HTML content with BeautifulSoup
        try:
            soup = BeautifulSoup(html_content, 'lxml')
        except Exception as e:
            self.logger.error(f'Error parsing HTML content: {e}')
            return []

        entities = []
        # Loop through divs with class 'mb-1' to find the data
        for div in soup.select('div.mb-1'):
            text = div.get_text(strip=True)

            # Parse multi-valued categories
            for category, field in self.entity_categories.items():
                if category in text:
                    for a in div.select('a.sidebar-link'):
                        # Create Entity Item (Composer, Artist, Orchestra, etc.)
                        new_entity = EntityItem()
                        new_entity['name'] = a.get_text(strip=True)
                        new_entity['href'] = a['href']
                        new_entity['id'] = a['href'].split('/')[-1]
                        new_entity['role'] = field
                        entities.append(new_entity)
                    break

        return entities

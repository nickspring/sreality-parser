import json
import os

import scrapy

from src.items import SrealityParserItem


class SrealitySpider(scrapy.Spider):
    """Sreality.cz simple parser"""

    name = "sreality"
    items_to_collect = int(os.getenv("ADS_NUMBER", 500))

    collected_count = 0
    current_page = 0

    def next_page_url(self):
        if self.collected_count >= self.items_to_collect:
            return None
        self.current_page += 1
        return os.getenv("URL_PATTERN").format(page=self.current_page)

    def start_requests(self):
        next_page = self.next_page_url()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse(self, response):
        json_response = json.loads(response.text)
        items = [
            SrealityParserItem(
                title=estate.get("name"),
                image=next(
                    iter(estate.get("_links", {}).get("images", [])),
                    {},
                ).get("href"),
            )
            for estate in json_response.get("_embedded", {}).get("estates", [])
        ]

        # traverse items
        for item in items:
            # if we have needed count break the cycle
            if self.collected_count >= self.items_to_collect:
                break

            # yield Item
            yield item
            self.collected_count += 1

        # get next page and yield it
        next_page = self.next_page_url()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

# Note I am _not_ using any of the scraping ability of pyquery, only its jquery like interface for selecting elements
# from an already retrieved web page
from pyquery import PyQuery

from crawler.links.link import Link, InvalidPathError, UnknownSchemeError


class LinkExtractor:
    """Extracts links from the text of a web page
    """
    def extract(crawled_page_url, page_text):
        """Given a web page will extract all <a> links, turn them into crawler.links.link.Link instances
           and return the results.

           Note: Will silently ignore all invalid (semantically, not whether they lead somewhere) links, and all
                Links with an unknown url scheme

           Args:
               crawled_page_url (string): The url of the crawled page
               page_text (string): The web page text

           Returns:
               list: List of crawler.links.link.Link instances representing every unique link on the page
        """

        parsed_page = PyQuery(page_text)
        links = []

        anchor_elements = parsed_page("a[href]")
        for anchor_element in anchor_elements:
            try:
                link = Link(crawled_page_url, anchor_element.attrib["href"])
                links.append(link)
            except (InvalidPathError, UnknownSchemeError):
                next

        return links

import logging

from crawler.site_map import SiteMap
from crawler.links.link import Link
from crawler.pages.page_fetcher import PageFetcher


class Crawler:
    """Crawls the given domain

        Attributes:
            site_map: The site map of the crawled domain.
    """
    site_map = None

    def __init__(self, start_domain):
        """Initialiser

            Args:
                start_domain (string): The domain to start crawling
        """
        self._start_link = Link(start_domain, "/")
        self.site_map = SiteMap()
        self._links_to_visit = set()

    def crawl(self):
        """Crawl the domain
        """
        logging.info("Fetching: {}".format(self._start_link))
        start_page = PageFetcher.get(self._start_link)

        self.site_map.add_page(start_page)

        self._links_to_visit = self._determine_links_to_visit(start_page)

        while len(self._links_to_visit) != 0:
            self._crawl_remaining_pages()

    def _crawl_remaining_pages(self):
        """After the first page has been crawled, spider out and crawl all out links within our subdomain which haven't
            yet been visited
        """
        new_links_to_visit = set()
        visited_links = set()

        for link in self._links_to_visit:
            logging.info("Fetching: {}".format(link))
            page = PageFetcher.get(link)
            visited_links.add(link)
            self.site_map.add_page(page)
            new_links_to_visit.update(self._determine_links_to_visit(page))

        self._links_to_visit.update(new_links_to_visit)
        # Remove the now visited links
        self._links_to_visit.difference_update(visited_links)

    def _determine_links_to_visit(self, page):
        """Get the links we still need to visit from the page.

            Args:
                page (crawler.pages.page.Page): The page to extract the links from

            Returns:
                list: List of crawler.links.link.Link, only includes links which are inside the subdomain and still
                      not yet visited
        """
        links_to_visit = set()
        for link in page.out_links:
            if link.in_crawled_domain() and not self.site_map.link_already_visited(link):
                links_to_visit.add(link)

        return links_to_visit

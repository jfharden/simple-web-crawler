import requests

from crawler.pages.page import Page


class PageFetcher:
    """Gets pages
    """
    def get(link):
        """Get the page at the specified link

            Args:
                link (crawler.links.link.Link): The link to fetch

            Returns:
                crawler.pages.page: The page
        """
        response = requests.get(link.url)

        return Page(link, response)

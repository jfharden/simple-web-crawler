from crawler.links.link_extractor import LinkExtractor


class Page:
    """Represents a single web page

    Attributes:
        link: The link that describes this page
        out_links: The links that describe all the anchor links out from this page
    """
    link = None
    out_links = None

    def __init__(self, link, page_text):
        """Initialiser

            Args:
                link: The link that describes this page
                page_text: The text of the page
        """
        self.link = link
        self._page_text = page_text

        self.out_links = LinkExtractor.extract(self.link.url, page_text)

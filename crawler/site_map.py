class SiteMap:
    """Map of the site
    """
    def __init__(self):
        self._visited_links = dict()

    def link_already_visited(self, link):
        """Has a link already been visited

            Args:
                link (crawler.links.link.Link): The link to check

            Returns:
                bool: True if link already visited
        """
        return link in self._visited_links

    def page_for_link(self, link):
        """Get the page for an already visited link

            Args:
                link (crawler.links.link.Link): The link for the page to return

            Returns:
                crawler.pages.page.Page: The visited page
        """
        return self._visited_links[link]

    def add_page(self, page):
        """Add a page to the site map

            Args:
                page (crawler.pages.page.Page): The page to add
        """
        self._visited_links[page.link] = page

    def all_pages(self):
        """ Get all pages in the sitemap

            Returns:
                list: list of crawler.pages.page.Page instances
        """
        return self._visited_links.values()


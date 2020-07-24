import unittest

from crawler.links.link import Link
from crawler.pages.page import Page
from unittest.mock import patch


class TestPage(unittest.TestCase):
    @patch("crawler.pages.page.LinkExtractor.extract", return_value=[
        Link("http://www.example.com", "foo/index.html"),
        Link("http://www.example.com", "bar/index.html"),
    ])
    def test_link(self, mock_link_extractor):
        link = Link("http://www.example.com/", "index.html")
        page = Page(link, "mocked_page_body")

        self.assertEqual(page.link, link)
        mock_link_extractor.assert_called_with("http://www.example.com/index.html", "mocked_page_body")

    @patch("crawler.pages.page.LinkExtractor.extract", return_value=[
        Link("http://www.example.com", "foo/index.html"),
        Link("http://www.example.com", "bar/index.html"),
    ])
    def test_out_links(self, mocked_link_extractor):
        link = Link("http://www.example.com/", "index.html")
        page = Page(link, "mocked_page_body")

        self.assertEqual(page.out_links, [
            Link("http://www.example.com", "foo/index.html"),
            Link("http://www.example.com", "bar/index.html"),
        ])

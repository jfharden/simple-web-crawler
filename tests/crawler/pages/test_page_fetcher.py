import requests
import responses
import unittest

from crawler.links.link import Link
from crawler.pages.page_fetcher import PageFetcher
from unittest.mock import patch


class TestPageFetcher(unittest.TestCase):
    MOCK_PAGE = """
        <html>
        <head>
            <title>Test Page Two Links</title>
        </head>
        <body>
            <p>
                <a href="http://www.example.com/foo.html">FooPage</a>
            </p>
            <div>
                <div>
                    <div>
                        <div>
                            <a href="https://www.example.com/sub/page/bar.html">BarPage</a>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
    """

    @responses.activate
    def test_get(self):
        responses.add(**{
            "method": responses.GET,
            "url": "http://www.example.com/index.html",
            "body": TestPageFetcher.MOCK_PAGE,
            "status": 200,
            "content_type": "application/html",
        })

        expected_out_links = [
                Link("http://www.example.com/index.html", "/foo.html"),
                Link("http://www.example.com/index.html", "/sub/page/bar.html"),
        ]
        expected_link = Link("http://www.example.com/", "index.html")

        actual_page = PageFetcher.get(Link("http://www.example.com/", "index.html"))

        self.assertEqual(actual_page.link, expected_link)
        self.assertEqual(actual_page.out_links, expected_out_links)

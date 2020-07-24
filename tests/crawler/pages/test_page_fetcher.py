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

    @patch("crawler.pages.page_fetcher.requests.get", return_value=MOCK_PAGE)
    def test_get(self, mock_requests_get):
        expected_out_links = [
                Link("http://www.example.com/index.html", "/foo.html"),
                Link("http://www.example.com/index.html", "/sub/page/bar.html"),
        ]
        expected_link = Link("http://www.example.com/", "index.html")

        actual_page = PageFetcher.get(Link("http://www.example.com/", "index.html"))

        self.assertEqual(actual_page.link, expected_link)
        self.assertEqual(actual_page.out_links, expected_out_links)
        mock_requests_get.assert_called_with("http://www.example.com/index.html")

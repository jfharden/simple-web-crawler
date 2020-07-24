import unittest

from crawler.links.link_extractor import LinkExtractor
from crawler.links.link import Link


class TestLinkExtractor(unittest.TestCase):
    def setUp(self):
        self.crawled_page_url = "http://www.example.com"

    def test_extract_one_link(self):
        page = """
        <html>
        <head>
            <title>Test Page One Link</title>
        </head>
        <body>
            <p>
                <a href="http://www.example.com/foo.html">FooPage</a>
            </p>
        </body>
        </html>
        """
        expected_links = [
            Link(self.crawled_page_url, "/foo.html"),
        ]

        actual_links = LinkExtractor.extract(self.crawled_page_url, page)

        self.assertEqual(actual_links, expected_links)

    def test_extract_multiple_links(self):
        page = """
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
        expected_links = [
            Link(self.crawled_page_url, "/foo.html"),
            Link(self.crawled_page_url, "/sub/page/bar.html"),
        ]

        actual_links = LinkExtractor.extract(self.crawled_page_url, page)

        self.assertEqual(actual_links, expected_links)

    def test_extract_relative_urls(self):
        page = """
        <html>
        <body>
            <p>
                <a href="foo.html">FooPage</a>
            </p>
            <div>
                <div>
                    <div>
                        <div>
                            <a href="/sub/page/../bar.html">BarPage</a>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        expected_links = [
            Link(self.crawled_page_url, "/foo.html"),
            Link(self.crawled_page_url, "/sub/bar.html"),
        ]

        actual_links = LinkExtractor.extract(self.crawled_page_url, page)

        self.assertEqual(actual_links, expected_links)

    def test_extract_includes_external_links(self):
        page = """
        <html>
        <body>
            <p>
                <a href="http://www.example.com/foo.html">FooPage</a>
                <a href="http://example.com/bar.html">BarPage</a>
                <a href="http://www.example.net/baz.html">BazPage</a>
            </p>
        </body>
        </html>

        """
        expected_links = [
            Link(self.crawled_page_url, "/foo.html"),
            Link(self.crawled_page_url, "http://example.com/bar.html"),
            Link(self.crawled_page_url, "http://www.example.net/baz.html")
        ]

        actual_links = LinkExtractor.extract(self.crawled_page_url, page)

        self.assertEqual(actual_links, expected_links)

    def test_discards_invalid_links(self):
        page = """
        <html>
        <body>
            <p>
                <a href="ftp://www.example.com/foo.html">FooPage</a>
                <a href="example.com/../../bar.html">BarPage</a>
                <a href="/baz.html">BazPage</a>
            </p>
        </body>
        </html>

        """
        expected_links = [
            Link("http://www.example.com", "/baz.html"),
        ]

        actual_links = LinkExtractor.extract(self.crawled_page_url, page)

        self.assertEqual(actual_links, expected_links)

    def test_extract_no_links(self):
        page = """
        <html>
        <body>
        </body>
        </html>
        """
        expected_links = []

        actual_links = LinkExtractor.extract(self.crawled_page_url, page)
        self.assertEqual(actual_links, expected_links)

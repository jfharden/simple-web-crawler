import unittest

from crawler.links.link import Link, InvalidPathError, UnknownSchemeError


class TestLink(unittest.TestCase):
    def setUp(self):
        self.crawled_page = "http://www.example.com"

    def test_init_with_unknown_scheme(self):
        with self.assertRaises(UnknownSchemeError):
            Link(self.crawled_page, "foo://127.0.0.1")

    def test_repr(self):
        self.assertEqual(
            repr(Link(self.crawled_page, "/foo/bar.html")),
            "http://www.example.com/foo/bar.html",
        )

    def test_hash(self):
        self.assertEqual(
            Link(self.crawled_page, "/foo/bar.html").__hash__(),
            hash("www.example.com/foo/bar.html"),
        )

    def test_init_with_simple_absolute_path_that_escapes_root(self):
        with self.assertRaises(InvalidPathError):
            Link(self.crawled_page, "http://www.example.com/../foo.html")

    def test_init_with_complex_absolute_path_that_escapes_root(self):
        with self.assertRaises(InvalidPathError):
            Link(self.crawled_page, "http://www.example.com/path/../foo/../../index.html")

    def test_init_with_simple_relative_path_that_escapes_root(self):
        with self.assertRaises(InvalidPathError):
            Link(self.crawled_page, "../foo.html")

    def test_init_with_complex_relative_path_that_escapes_root(self):
        with self.assertRaises(InvalidPathError):
            Link(self.crawled_page, "/path/foo/../../../bar.html")

    def test_url_simple_relative_url(self):
        self.assertEqual(
            Link(self.crawled_page, "index.html").url,
            "http://www.example.com/index.html",
        )

    def test_url_crawled_subpage_relative_url(self):
        self.assertEqual(
            Link("http://www.example.com/sub/path/index.html", "foo.html").url,
            "http://www.example.com/sub/path/foo.html",
        )

    def test_url_complex_relative_url(self):
        self.assertEqual(
            Link(self.crawled_page, "/sub/path/../path/index.html").url,
            "http://www.example.com/sub/path/index.html",
        )

    def test_url_simple_absolute_url_same_domain(self):
        self.assertEqual(
            Link(self.crawled_page, "http://www.example.com/index.html").url,
            "http://www.example.com/index.html",
        )

    def test_url_simple_absolute_url_different_domain(self):
        self.assertEqual(
            Link(self.crawled_page, "http://www.example.net/index.html").url,
            "http://www.example.net/index.html",
        )

    def test_url_simple_absolute_url_different_port(self):
        self.assertEqual(
            Link(self.crawled_page, "http://www.example.net:123/index.html").url,
            "http://www.example.net:123/index.html",
        )

    def test_in_crawled_domain(self):
        link = Link(self.crawled_page, "")
        self.assertTrue(link.in_crawled_domain())

    def test_in_crawled_domain_with_relative_path(self):
        link = Link(self.crawled_page, "foo.html")
        self.assertTrue(link.in_crawled_domain())

    def test_in_crawled_domain_with_absolute_path(self):
        link = Link(self.crawled_page, "http://www.example.com/foo.html")
        self.assertTrue(link.in_crawled_domain())

    def test_in_crawled_domain_with_absolute_path_different_port(self):
        link = Link(self.crawled_page, "http://www.example.com:123/foo.html")
        self.assertTrue(link.in_crawled_domain())

    def test_in_crawled_domain_different_scheme(self):
        link = Link(self.crawled_page, "https://www.example.com/foo.html")
        self.assertTrue(link.in_crawled_domain())

    def test_in_crawled_domain_parent_domain(self):
        link = Link(self.crawled_page, "http://example.com/foo.html")
        self.assertFalse(link.in_crawled_domain())

    def test_in_crawled_domain_different_tld(self):
        link = Link(self.crawled_page, "http://www.example.net/")
        self.assertFalse(link.in_crawled_domain())

    def test_in_crawled_domain_different_subdomain(self):
        link = Link(self.crawled_page, "http://foo.example.net/")
        self.assertFalse(link.in_crawled_domain())

    def test_equal_simple(self):
        self.assertEqual(
            Link(self.crawled_page, ""),
            Link(self.crawled_page, ""),
        )

    def test_equal_same_path(self):
        self.assertEqual(
            Link(self.crawled_page, "index.html"),
            Link(self.crawled_page, "index.html"),
        )

    def test_equal_same_absolute_path(self):
        self.assertEqual(
            Link(self.crawled_page, "http://www.example.com/index.html"),
            Link(self.crawled_page, "http://www.example.com/index.html"),
        )

    def test_equal_same_absolute_path_and_relative_path(self):
        self.assertEqual(
            Link(self.crawled_page, "http://www.example.com/index.html"),
            Link(self.crawled_page, "index.html"),
        )

    def test_equal_different_scheme(self):
        self.assertEqual(
            Link(self.crawled_page, "http://www.example.com/index.html"),
            Link(self.crawled_page, "https://www.example.com/index.html"),
        )

    def test_equal_different_path(self):
        self.assertNotEqual(
            Link(self.crawled_page, "index.html"),
            Link(self.crawled_page, "index.htm"),
        )

    def test_equal_different_port(self):
        self.assertNotEqual(
            Link(self.crawled_page, "index.html"),
            Link(self.crawled_page, "index.htm"),
        )

    def test_equal_different_subdomain(self):
        self.assertNotEqual(
            Link(self.crawled_page, "http://www.example.com/index.html"),
            Link(self.crawled_page, "http://foo.example.com/index.html"),
        )

    def test_equal_different_tld(self):
        self.assertNotEqual(
            Link(self.crawled_page, "http://www.example.com/index.html"),
            Link(self.crawled_page, "http://www.example.net/index.html"),
        )

    def test_equal_different_equivalent_complex_path(self):
        self.assertEqual(
            Link(self.crawled_page, "http://www.example.com/sub/path/../foo/bar.html"),
            Link(self.crawled_page, "http://www.example.com/sub/foo/bar.html"),
        )

    def test_equal_different_not_equivalent_complex_path(self):
        self.assertNotEqual(
            Link(self.crawled_page, "http://www.example.com/sub/path/../foo/bar.html"),
            Link(self.crawled_page, "http://www.example.net/sub/path/bar.html"),
        )

    def test_equal_crawled_subpage_relative_url(self):
        self.assertEqual(
            Link("http://www.example.com/sub/path/index.html", "foo.html"),
            Link("http://www.example.com/index.html", "sub/path/foo.html"),
        )


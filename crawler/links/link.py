import os.path

from urllib.parse import urlparse


class InvalidPathError(ValueError):
    pass


class UnknownSchemeError(ValueError):
    pass


class Link:
    """Represents a Link on a page, links are equivalent in the following circumstances:
        * They have the same domain
        * They have the same path (after being resolved to an absolute path)
        * They may have diffenent schemes (so https and http of the same link are considered equivalent)
        * They may not have a different port (so www.example.com and www.example.com:123 are considered different

        Attributes:
            url (string): The complete url, either as the normalised original href (if the path was absolute) or as
                derived from combining the href of the link with the page being crawled (if the href is relative)

        # Design note: This class is pretty complex, but knowing any old nonsense can be in the href of the links
                       on webpages, and my desire to ensure I can _know_ that different looking hrefs lead to the same
                       ultimate page (and to be able to easily compare two different links, no matter what they look
                       like, and no matter where we are in the website heirachy) leads to this complexity. If this
                       class can be comprehensive and correct then it makes the rest of this task _much_ easier and
                       makes it trivial to avoid graphing loops when traversing a heirarch of pages.
    """
    url = None

    def __init__(self, crawled_page, href):
        """Initialise

        Args:
            crawled_page: The domain that is being crawled, used to construct links from relative urls
            href: The href of the link to parse

        Raises:
            InvalidPathError: If the href tries to escape the root of the domain
            UnknownSchemeError: If the href is an unknown url scheme (only http, and https are known)
        """
        self._raw_crawled_page = crawled_page
        self._raw_href = href

        self.crawled_scheme, self.crawled_netloc, self.crawled_path, _, _, _ = urlparse(crawled_page)
        self.scheme, self.netloc, self.path, _, _, _ = urlparse(href)

        self._raw_scheme = self.scheme
        if self.scheme == "":
            self.scheme = self.crawled_scheme

        self._raw_netloc = self.netloc
        if self.netloc == "":
            self.netloc = self.crawled_netloc

        # Parse the domains and ports
        self.crawled_domain, self.crawled_port = self._parse_netloc(self.crawled_netloc, self.crawled_scheme)
        self.domain, self.port = self._parse_netloc(self.netloc, self.scheme)

        # Parse the subpaths
        self.crawled_subdir = self._parse_subdir(self.crawled_path)
        self.subdir = self._parse_subdir(self.path)

        # Construct our final absolute path
        if self._is_relative_path():
            self.absolute_path = self._join_paths(self.crawled_subdir, self.path)
        else:
            self.absolute_path = self.path

        # Test for paths that are escaping from the root of the domain
        self.normalised_netloc_and_path = self._join_netloc_and_path()
        self.url = self._construct_url()

    def in_crawled_domain(self):
        """Check if the link is within the originally crawled domain

        Returns:
            bool: True if the Link is within the crawled domain
        """
        return self.domain == self.crawled_domain

    def _join_paths(self, subdir, path):
        """Joins a subdir with a path to produce a clean, absolute path

        """
        abspath = self._path_to_abspath(path)
        if subdir == "":
            return abspath
        else:
            return "{subdir}{abspath}".format(
                subdir=subdir,
                abspath=abspath,
            )

    def _path_to_abspath(self, path):
        if path.startswith("/"):
            return path
        
        return "/{}".format(path)

    def _construct_url(self):
        """Return a parsed and cleaned url

        Returns:
            string: The parsed and cleaned url with only scheme, domain, port, and path parts
        """
        if self.scheme == "":
            scheme_separator = ""
        else:
            scheme_separator = ":"

        return "{scheme}{scheme_separator}//{netloc_and_path}".format(
            scheme=self.scheme,
            scheme_separator=scheme_separator,
            netloc_and_path=self.normalised_netloc_and_path
        )

    def _join_netloc_and_path(self):
        """Join the netlocation and the path together and normalise the path

        Returns:
            None

        Raises:
            InvalidPathError: Raised if the path tries to escape the root of the domain (like
                www.example.com/../../foo.html)
        """

        # If we join the netloc and the absolute path together and then normalise the string,
        # if does not start with the netloc we know there was enough upwards directory
        # traversal to escape from the root
        netloc_and_path = "{netloc}{path}".format(netloc=self.netloc, path=self.absolute_path)
        normalised_url = os.path.normpath(netloc_and_path)

        if not normalised_url.startswith(self.netloc):
            raise InvalidPathError()

        return normalised_url

    def _is_relative_path(self):
        """Checks if the href is a relative path

        Returns:
            bool: True if the href was a relative url
        """
        href_is_relative = not self._raw_href.startswith("/")

        return self._raw_netloc == "" and href_is_relative

    def _parse_subdir(self, path):
        """Parses the subdir from the filepath

        Args:
            path (string): The path from the url

        Returns:
            string: The subdirectory the path includes
        """
        return os.path.dirname(path)

    def _parse_netloc(self, netloc, scheme):
        """Parse a netloc to a domain and port

        Args:
            netloc (string): The netloc of the url
            scheme (string): The original scheme of the url

        Returns:
            tuple(domain: str, port: int): The domain and port
        """
        if ":" in netloc:
            return tuple(netloc.split(":"))
        else:
            return (
                netloc,
                self._default_port_for_scheme(scheme),
            )

    def _default_port_for_scheme(self, scheme):
        """Returnt the default port for a particular scheme
        """
        scheme_lower_case = scheme.lower()

        if scheme_lower_case == "http":
            return 80
        elif scheme_lower_case == "https":
            return 443
        else:
            raise UnknownSchemeError("Unknown scheme {}".format(scheme))

    def __repr__(self):
        return self.url

    def __hash__(self):
        """We are implementing this so we can keep a dict of all the visited links
           making it trivial, and O(1) operation to know if we have already crawled
        """
        return hash(self.normalised_netloc_and_path)

    def __eq__(self, other):
        return self.normalised_netloc_and_path == other.normalised_netloc_and_path

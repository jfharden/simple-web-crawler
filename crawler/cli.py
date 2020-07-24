import argparse
import logging

from crawler.crawler import Crawler


class CLI:
    """Coordinating class to run the CLI
    """
    def run():
        """Execute the cli action

        Returns:
            None
        """
        parser = argparse.ArgumentParser(description="Simple one domain web crawler by Jonathan Harden")

        parser.add_argument(
            "domain",
            help="Domain to crawl (will not leave the subdomain specified and will ignore any path part)",
        )
        parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="Verbose, print INFO level logging",
        )

        args = parser.parse_args()

        if args.verbose:
            logging.basicConfig(level=logging.INFO)

        crawler = Crawler(args.domain)
        crawler.crawl()

        for page in crawler.site_map.all_pages():
            print("Page: {}".format(page.link))
            print("    Outbound Links:")
            for out_link in set(page.out_links):
                print("        {}".format(out_link))

            print("\n\n")

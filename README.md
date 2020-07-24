# simple-web-crawler
Simple 1 sub-domain web crawler

## Requirements

* Python 3.8

## Usage

Activate the virtual env first:

`source env/bin/activate`

Then run the crawler (using -v will print an INFO message showing you which pages are currently being fetched):

`./crawl.py -v <domain>`

## Running tests

`python -m unittest discover`

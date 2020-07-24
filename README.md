# simple-web-crawler
Simple 1 sub-domain web crawler

## Notes
It takes quite a while to crawl a large site like Monzo, I could have sped this up a _lot_ using a
ThreadPoolExecutor and using futures (it's waiting for the pages to be retrieved which takes the time, which is a
perfect case for futures even with pythons global interpreter lock). However I had already spent a little more than the
4 hours on the task so I thought it better not to.

The Link class is quite complex, but keeping the complexity within that class makes everything else fall out easily, I
can compare the links as equal to each other with == (which also enables a lot of langauge features like being able to
assertEqual easily). I've also implemented the \_\_hash\_\_ method which means I have a custom algorithm for python to
decide how to hash my instances, this allows me to use the instances as keys in a dict (those keys are the simple
inbuilt hash algorithm, but performed on the URL after I have normalised it and ignore differences in the scheme (I
chose to see http and https as equivalent pages, especially since the requests library will automatically follow 301
and 302 redirects)). Combining implenting custom equality and custom hashing means I can use the class as elements of
the built in set class making it _super_ trivial to remove non-unique links.

I put a _LOT_ of tests on the Link class knowing how deep the complexity is in there, my aim was to try and flex every
possible combination of domains and paths. No surprise I caught a couple of bugs with the tests (which I wrote prior to
the class)

I considered implementing this in go, I've previously written some tests in go which drive web requests using goquery
to perform openid authentication as a client 
(see https://github.com/jfharden/template-php-docker-site/blob/master/test/openid_helper.go). I decided not to do this
in go though since it was time limited and I know python a _lot_ better than go, so my time would be better served. As
it happens after implementing the link class I think I made the right choice since all the string and url manipulation
would have been a lot more painful in go.

Thanks for reading!

## Requirements

* Python 3.8

## Usage

Activate the virtual env first and install the requirements:

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Then run the crawler (using -v will print an INFO message showing you which pages are currently being fetched):

Note: You must include the scheme (e.g. http, or https), for example http://www.example.com

`./crawl.py -v <domain>`

## Running tests

`python -m unittest discover`

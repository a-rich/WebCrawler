WebCrawler
================

Dependencies
----------------
* python3 -- version 3.4.3
* bs4 (beautifulsoup4) -- version 4.5.1
* requests -- version 2.11.1
* validators -- 0.11.1

Description
----------------
WebCrawler.py is composed of two parts -- the class 'WebCrawler' and the main
script.

###WebCrawler class
The class variables are:
* a `crawlQueue` which is a list of links that have yet to be visited
* a `limit` which is the number of links to be visited before the crawler halts
  -- the default is 100
* an `out_file` which is a string of the file name which will have the visited
  links written to it -- the default `out_file` is "visited.txt"
* a `visited` dictionary which has `True` as a value for every key (URL) that
  has been visited
* and a `count` integer that is compared with `limit` before dequeuing the
  `crawlQueue`

The class initialized with default values for `limit` and `out_file`, but the
user must provide a seed URL via the command-line (string URL after the "-u"
flag). The class initialization method will parse the seed URL and begin
crawling.

The class has two methods: `parseLinks` and `crawl`. `parseLinks` uses
BeautifulSoup to find all anchor tags (an if condition is used here to add an
additional parameter that's required to traverse the Wikipedia web graph). For
each anchor tag that has a href attribute, `parseLinks` will, if necessary,
prepend the host to the path for internal links and strip off query strings
from the URL -- then, if the link is valid and is not already in `crawlQueue`
or `visited`, the link is enqueued. `crawl` will, while `crawlQueue` is
not empty and `count` < `limit`, dequeue the next link from `crawlQueue` and
call `parseLinks` on it. Then it adds that link to `visited` and increments
`count`. Once the while loop terminates, `crawl` opens `out_file` and writes
all the visited pages in `visited` to it.

###Main script
The top-level script of `WebCrawler` sets the default `limit` to 100 and the
default `out_file` to "visited.txt". It then parses all the command-line
arguments (sys.argv) and assigns to `url` the argument that succeeds the "-u"
flag, assigns to `limit` the argument that succeeds the "-l" flag, and assigns
to `out_file` the argument that succeeds the "-o" flag. So long as the seed URL
is valid, `WebCrawler` is initialized.

Instructions
----------------
Simply run the python file like so:
`python3 WebCrawler.py -u "<URL (STRING)>"`

This will use <VALID URL> as the seed URL and traverse the first 100 links the
crawler finds.

If you want to have the crawler traverse more or less than a 100 links, run:
`python3 WebCrawler.py -u "<URL (STRING)>" -l <LIMIT (INTEGER)>`

If you want to `WebCrawler` to save visited pages to a file other than
"visited.txt", run:
`python3 WebCrawler.py -u "<URL (STRING)>" -o <OUT_FILE (STRING)>`

If you wish to terminate the graph traversal prematurely, on Linux you can
press `CTRL + \` to issue the `SIGQUIT` signal. Although it hasn't been tested,
`CTRL + BREAK` and `CTRL + C` should send the `SIGBREAK` and `SIGINT` signals
respectively which may or may not terminate the execution on Mac and/or
Windows.

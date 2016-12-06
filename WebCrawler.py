from sys import argv, exit
from bs4 import BeautifulSoup, SoupStrainer
from requests import get
from validators import url as validate_url

class WebCrawler:
  crawlQueue = []   # List of stored links to be visited still.
  limit = 0         # Number of links to visit before halting (default is 100).
  out_file = None   # File to write visited pages to.
  visited = {}      # Map of links already added to CRAWLQUEUE.
  count = 0         # Count of links visited.

  def __init__(self, url, limit, out_file):
    self.limit = limit
    self.out_file = out_file
    self.parseLinks(url)
    self.crawl()

  def parseLinks(self, url):
    # Appends to CRAWLQUEUE the valid links on the page that URL links to.
    try:
      links = BeautifulSoup(get(url).text, 'lxml').findAll("a", href=True)
      for l in links:
        if l['href'].split('/')[0] == '':
          # Prepends host to path to make internal links valid.
          link = ''.join([url, l['href']])
        else:
          link = l['href']
        link = link.rsplit('?', 1)[0]  # Removes query strings from URL.
        if validate_url(link) and link not in self.crawlQueue and link not in self.visited:
          self.crawlQueue.append(link)
    except:
      pass

  def crawl(self):
    print("Crawling...\nLink\t:\t# of links in queue\t:\t# of links visited")
    try:
      while self.crawlQueue and self.count < self.limit:
        nextLink = self.crawlQueue.pop(0)
        self.parseLinks(nextLink)
        self.visited[nextLink] = True
        self.count += 1
        print(nextLink, ":", len(self.crawlQueue), ":", self.count)
    except KeyboardInterrupt:
      exit()
    with open(out_file, 'w') as f:
      for page in self.visited:
        f.write(page+'\n')


# Script main.
if __name__ == "__main__":
  url = None                # Seed URL.
  limit = 100               # Default limit for # of pages to visit.
  out_file = "visited.txt"  # File where visited pages are saved to.

  for i, arg in enumerate(argv):
    if arg == "-u":
      try:
        url = argv.pop(i+1)
      except:
        pass

    if arg == "-l":
      try:
        limit = int(argv.pop(i+1))
      except ValueError:
        print("Error: the LIMIT amount you provided wasn't an integer.")
        exit()

    if arg == "-o":
      try:
        out_file = argv.pop(i+1)
      except:
        pass

  # If URL is valid, begin crawling.
  if url:
    if validate_url(url):
      WebCrawler(url, limit, out_file)
    else:
      print("Error: the URL you provided is not valid (make sure you include 'http://' or 'https://').")
  else:
    print("Error: you must provide a valid URL (string) following the '-u' flag.")

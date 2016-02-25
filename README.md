# jaw

All scrapers have two layers: the layer that actually gathers data from individual
pages, and the layer that navigates the site we are trying to scrape.
jaw concerns the latter. Specifically, jaw complements jess. Given a site, a seed, 
and an indication of the types of pages you want to scrape jaw will handle moving 
through the site and returning the soups for pages that match your criteria, all 
while making sure that every page reachable from your seed that fits your criteria 
can be reached in your program while ensuring that you never get any duplicates.

The Details

Open guide/guide.html in your favorite browser to get a more detailed look at jaw.

Dependencies

 * BeautifulSoup
 * lxml

Installation

Download the repository and inside it run: python setup.py install

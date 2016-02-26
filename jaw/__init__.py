import re
from urllib2 import urlopen
from bs4 import BeautifulSoup

class Issue(Exception):
    def __init__(self, problem):
        self.problem = problem
    def __str__(self):
        return 'ERROR: the problem was: %s' % self.problem

"""
The following class allows us to keep track of the soups that we gather
as if they are nodes in a tree, so we can always go back to the parent
"""

class Step:

    # parent is the parent step, and soup is the current soup for this step
    def __init__(self, parent, soup):
        self.parent = parent
        self.soup = soup

"""
Refer to the guide
"""

class Teleportation:

    def __init__(self, base_url, link_tests=[], soup_tests=[], link_hashes=[], soup_hashes=[]):
        # first we are going to create a link test that checks that the domain
        # name is correct
        self.base_url = base_url
        self.expre = re.compile('^%s' % base_url)
        base_url_test = self.base_url_test
        # now we create the link_tests and soup_tests list
        self.link_tests = link_tests + [base_url_test]
        self.soup_tests = soup_tests
        # now we have the hash lists
        self.link_hashes = link_hashes
        self.soup_hashes = soup_hashes
        self.current_step = None
        self.count = 0
        self.current_link = ''

    def base_url_test(self, link):
        # first we try to make sure the link starts with the base_url
        match = re.search(self.expre, link)
        if not match:
            # if it doesn't we check to see if it is a relative url
            if link[0] == '/':
                # then we are all good concerning this test
                return True
            else:
                # houstan, we have a problem
                return False
        else:
            return True

    def checkLink(self, link):
        # this is a method that will check that the link passes
        # our link_tests
        for test in self.link_tests:
            if test(link) == False:
                return False
        return True

    def checkSoup(self, soup):
        for test in self.soup_tests:
            if test(soup) == False:
                return False
        return True

    def makeLinkAbsolute(self, link):
        # this checks to see if a link is relative, and if it
        # is goes ahead sticks the base url on the front
        if link[0] == '/':
            link = self.base_url + link
        return link

    def getSoup(self, link):
        # this simply takes the link (as a string)
        # and gets the corresponding soup
        # it is here we make the link absolute
        # it returns None if there was a problem
        link = self.makeLinkAbsolute(link)
        try:
            file = urlopen(link)
            html = file.read()
            soup = BeautifulSoup(html, 'lxml')
        except:
            soup = None
        return soup

    def Seed(self, link):
        # we are going to grab our first soup here
        soup = self.getSoup(link)
        if soup:
            # we set the current step to be the step containing our seed
            self.current_step = Step(None, soup)
            self.current_link = link
            # and then we return the soup
            return soup
        else:
            raise Issue('link you provided as a seed is invalid, no soup was obtained')

    def Teleport(self):
        if not self.current_step:
            print('current step is None, returning None to indicate all paths have been searched')
            return None
        # first we get the link tags in our soup
        link_tags = self.current_step.soup.find_all('a')
        # now we iterate through them
        for tag in link_tags:
            # next we try to get their href attribute
            try:
                link = tag.attrs['href']
            except:
                # in this case we just continue onto the next link tag
                continue
            # next we are going to put the link through our tests
            if not self.checkLink(link):
                # one of the tests wasn't passed so we move onto the next tag
                continue
            # now we check to make sure we haven't found this already
            h = hash(link)
            if h in self.link_hashes:
                # in this case we go onto the next link
                continue
            # now we know we have a new link, so we record it in our hashes
            self.link_hashes.append(h)
            print('this is a new link that passed your tests: %s' % link)
            # alright so our link tests passed, now we try to get the soup from this
            soup = self.getSoup(link)
            # we check that the soup exists
            if not soup:
                # going to have to try the next tag
                continue
            # so now we check to make sure we haven't seen this soup before
            h = hash(soup.get_text())
            if h in self.soup_hashes:
                continue
            # we add it to the list of soups we have found
            self.soup_hashes.append(h)
            # now we put our soup through the soup tests
            if not self.checkSoup(soup):
                continue
            # everything has passed so this is our next step!
            next_step = Step(self.current_step, soup)
            # now we set our current step as this step
            self.current_step = next_step
            # we incremement the count and see if it is divisible by 10
            # if so we let the user know where they are at
            self.count += 1
            if self.count % 10 == 0:
                print('Pages reached so far: %s' % self.count)
            # and finally we return the soup that we have found
            print('the page at this link is new and passed your tests: %s' % link)
            self.current_link = link
            return soup
        # now if we get here it means that have searched every tag and
        # nothing has worked for us so we are going to have to go back
        # to the previous step. So we set the current_step to be this current_step's
        # parent and call this function again
        print('GOING BACK A STEP')
        parent_step = self.current_step.parent
        self.current_step = parent_step
        return self.Teleport()

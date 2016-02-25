from __init__ import Teleportation

def relativeLink(link):
    if link[0:9] != '/universe':
        return False
    else:
        return True

def normalLink(link):
    if link.find(':') != -1 or link.find("?") != -1:
        return False
    else:
        return True

def hasPowerBox(soup):
    tags = soup.select('.powergrid')
    if len(tags) > 1:
        return True
    else:
        return False

link_tests = [relativeLink, normalLink]
soup_tests = [hasPowerBox]
base_url = 'http://marvel.com'

tele = Teleportation(base_url, link_tests, soup_tests)
soup = tele.Seed('http://marvel.com/universe/Scarlet_Witch_%28Wanda_Maximoff%29')
while soup:
    soup = tele.Teleport()

print(count)

"""
Downloalds 'verbs' for downloading BeigeBook content
"""
from urllib import request
import os
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import pickle


base_url = 'http://www.minneapolisfed.org/bb/'
outfile = 'links.dat'


def get_year_link(year):
    """
    extract BeigeBook report links from FED's BegieBook yearly page 
    """

    url = base_url + 'bbresults.cfm'

    data = {'BB_District': 'National Summary', 'BB_Year': str(year),
            'BB_Qtr':'All'}

    data = urlencode(data).encode('utf-8')
    page = request.urlopen(url, data).read()
    soup = BeautifulSoup(page)

    links = []
    # append all 'report' links to list
    for link in soup.find_all('a'):
        href = link.get('href') or ''

        if href.startswith('reports'):
            links.append(base_url + href)

    return links


def get_links():
    """
    Saves all links to BeigeBooks in a pickle
    """
    years = range(1970, 2014)

    all_links = []
    for year in years:
        print(year)
        links = get_year_link(year)
        print(len(links))
        all_links.extend(links)

    with open(outfile, 'wb') as f:
        pickle.dump(all_links, f)

    print(len(all_links))


def dl_all():
    "loads pickled BeigeBook links and calls dl"

    with open(outfile, 'rb') as f:
        links = pickle.load(f)

    for link in links:
        print(link)
        try:
            dl(link)
        except:
            print('failed')


def dl(link):
    """
    saves a page content to data dir
    """
    fname = os.path.join('data', link.split('/')[-1])
    page = request.urlopen(link).read()

    with open(fname, 'wb') as f:
        f.write(page)

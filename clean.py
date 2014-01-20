"""
Functions for reading local BeigeBook content and saving to a list of
dictionaries using pickle.
"""

import os
from bs4 import BeautifulSoup, NavigableString, Tag
from collections import defaultdict
import pickle
from collections import Counter
import datetime
from itertools import chain
import re
import sys


data_file = 'dump.pkl'


def find_date(astring):
    """
    example string is:
         'Beige Book National Summary November 2, 1983'
    """
    regex = r"(\d{1,2}, \d{4})"
    matches = re.findall(regex, astring)
    if len(matches) == 1:
        return matches[0]
    return matches


def find_from_list(alist):
    return list(filter(None, map(find_date, alist)))


def get_soup(fname_path):
    with open(fname_path, 'rb') as f:
        data = f.read()
    return BeautifulSoup(data)


def extract_to_dict(soup):
    """
    Extract interesting parts to a dictionary, by section
    if no section saved in empty
    """
    # find h2 elemet, this is the content header
    h2s = soup.findAll('h2')
    assert len(h2s) == 1

    # sometimes h2 is nested in center or td
    parent = h2s[0].parent.parent

    ps = parent.findAll('p')

    d = defaultdict(list)
    title = 'empty'
    d[title].append(ps[0].text.strip())

    #for sib in start.next_siblings:
    for sib in ps:
        if not isinstance(sib, NavigableString):
            if not sib == None:

                # br mark the demarkation between sections
                if len(sib.findAll('br')) > 0:
                    # either extract b or strong
                    for br in sib.findAll('br'):
                        br.extract()

                    # title will change, set default
                    if len(sib.findAll('b')) == 1:
                        title = clean_text(sib.findAll('b')[0].text.strip().lower())
                        for b in sib.findAll('b'):
                            b.extract()

                    if len(sib.findAll('strong')) == 1:
                        title = clean_text(sib.findAll('strong')[0].text.strip().lower())
                        for t in sib.findAll('strong'):
                            t.extract()

                    d[title].append(sib.text.strip())

                else:
                    d[title].append(sib.text.strip())
    return clean_bb(d)


def pubdate_map(data_dict):
    datemap = {}
    for k in data_dict:
        date = get_date(k)

        fine_date = find_from_list(data_dict[k]['empty'])

        if len(fine_date) > 0:
            try:
                day = int(fine_date[0].split(',')[0])
                date = datetime.datetime(date.year, date.month, day)
            except:
                print(k)
                print(sys.exc_info())
        datemap[k] = date

    return datemap


def extract_all():
    ls = os.listdir('data/')
    d = {}
    for l in ls:

        soup = get_soup('data/' + l)
        try:
            d[l] = extract_to_dict(soup)
        except:
            print(l)

    with open('dump.pkl', 'wb') as f:
        pickle.dump(d, f)


def get_data():
    """
    :returns: dict of defaultdicts {'filename':{'section1': data, ...}}
    """
    with open(data_file, 'rb') as f:
        data = pickle.load(f)
    return data


def get_date(fname):
    dstring = fname[:5]
    d = datetime.datetime.strptime(dstring, '%y-%m')
    return d
    

def ranks(all_stats_data):
    rank = []
    c = Counter()
    for k in all_stats_data:
        c[all_stats_data[k][1]] += 1
        rank.append((k, all_stats_data[k][1]))

    rank = sorted(rank, key=lambda x: x[1], reverse=True)
    return rank, c
    

def clean_text(text):
    return ' '.join(text.split())


def stats(bb):
    """
    return keys and length of each item
    """

    sections = list(bb.keys())
    lengths = []
    types = []

    for s in sections:
        lengths.append(len(bb[s]))
        types.append(type(bb[s]))

    return list(zip(sections, lengths, types)), len(sections)


def all_stats(data):
    stats_d = {}
    for key in data.keys():
        bb = data[key]
        stats_d[key] = stats(bb)
    return stats_d


def clean_bb(bb):
    """
    a bb is a defaultdict([])
    """
    new_bb = {}
    for section in bb:
        bb[section] = list(map(clean_text, bb[section]))
        clean_section_title = clean_text(section).lower()

        clean_sections = list(map(clean_text, bb[section]))
        new_bb[clean_section_title] = clean_sections

    return new_bb


def clean(data_dict):

    for k in data_dict:
        bb = data_dict[k]
        bb = clean_bb(bb)
        data_dict[k] = bb
    return data_dict


def filtered(data_dict):
    new_dict = {}
    for k in data_dict:
        bb = data_dict[k]
        s, no_sections = stats(bb)
        if no_sections < 3:
            continue
        new_dict[k] = bb
    return new_dict


def save(data_dict):
    with open(data_file, 'wb') as f:
        pickle.dump(data_dict, f)

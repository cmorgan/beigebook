
from itertools import chain
import pandas as pd
import pysentiment as ps
import pickle

import clean


class BeigeBook(object):
    def __init__(self, file_name, data_dict, date_map):
        self.file_name = file_name
        self.date = date_map[file_name]
        self.sections = self.process_dict(data_dict)
        self._sentiment = None
    
    def process_dict(self, data_dict):
        "each section is one long string"
        new = {}
        for k in data_dict:
            new[k] = ' '.join(data_dict[k])
        return new

    @property
    def content(self):
        
        content = ''
        # join each part of a section
        lists = list(self.sections.values())
        return ' '.join(chain(lists))

    @property
    def sentiment(self):
        if not self._sentiment:
            self._sentiment = get_score(self.content)
        return self._sentiment
    
    def stats(self):
        number_of_words = len(self.content.split())

        return {'number_of_words': number_of_words,
                'number_of_sections': len(self.sections.keys()),}
                #'sentiment': self.sentiment}

    def as_record(self):
        ":returns: dictionary for input into DataFrame"
        data = {}
        # flatten bb.sentiment
        for type in self.sentiment.keys():
            for k, v in self.sentiment[type].items():
                data[type + '_' + k] = v
        data['date'] = self.date
        return data

    def __repr__(self):
        # summary of obj will be printed
        args = ",".join('%s=%r' % i for i in sorted(self.__dict__.items()) if
                        not i[0] in ['sections'])
        return '%s(%s)' % (self.__class__.__name__, args)


def construct_df(bbs):
    "construct DataFrame from BeigeBooks"
    return pd.DataFrame.from_records([bb.as_record() for bb in bbs],
                                     index='date').sort()


def all_bb():
    d = clean.get_data()
    s = get_scores()
    dm = clean.pubdate_map(d)
    bbs = []
    for k in d:
        bb = BeigeBook(k, d[k], dm)
        bb._sentiment = s[k]
        bbs.append(bb)
    return bbs


def get_scores():
    with open('scores.pkl', 'rb') as f:
        return pickle.load(f)


def get_df():

    bbs = all_bb()

    ts1 = dict([(bb.date, bb.stats()['number_of_words']) for bb in bbs])
    ts2 = dict([(bb.date, bb.stats()['number_of_sections']) for bb in bbs])

    # index = [bb.date for bb in bbs]
    # t1 = [bb.stats()['number_of_words'] for bb in bbs]
    # t2 = [bb.stats()['number_of_sections'] for bb in bbs]
    # data2 = {'number_of_words': t1, 'number_of_sections': t2}
    # df = pd.DataFrame(data2, index=index)

    data = {'number_of_words': ts1, 'number_of_sections': ts2}

    return pd.DataFrame(data)


def all_scores():
    """
    :returns: scores e.g. 

    '99-11-su.cfm': {'HIV4': {
                           'Negative': 42,
                           'Polarity': 0.3956,
                           'Positive': 97,
                           'Subjectivity': 0.2185},
                     'LM': {
                           'Negative': 38,
                           'Polarity': -0.3333,
                           'Positive': 19,
                           'Subjectivity': 0.0896}},
    """

    bbs = all_bb()
    scores = {}
    for bb in bbs:
        print(bb.file_name)
        scores[bb.file_name] = get_score(bb.content)
    return scores


def get_score(data):
    hiv4 = ps.HIV4()
    lm = ps.LM()
    tokens = hiv4.tokenize(data)
    score = hiv4.get_score(tokens)
    lm_score = lm.get_score(tokens)
    return dict([('HIV4', score), ('LM', lm_score)])

def get_tbill2():
    maturity_map = {
        1: "41e97c2acd1420d3a3ee55071da52e6a",
        3: "8a0cb4c31786ea79a513ab14cf2e5389",
        6: "6e140ed697a0c45297effbf7a1c3d5a5",
    }

    url = (
        "http://www.federalreserve.gov/datadownload/"
        "Output.aspx?rel=H15&series="
        "%s&lastObs=&from=&to=&"
        "filetype=csv&label=include&layout=seriescolumn" % maturity_map[3])

    df = pd.DataFrame.from_csv(url, header=5)

    return df

def get_tbill():
    maturity_map = {
        1: "41e97c2acd1420d3a3ee55071da52e6a",
        3: "8a0cb4c31786ea79a513ab14cf2e5389",
        6: "6e140ed697a0c45297effbf7a1c3d5a5",
    }

    big_df = pd.DataFrame()

    for m in maturity_map.keys():
        url = (
            "http://www.federalreserve.gov/datadownload/"
            "Output.aspx?rel=H15&series="
            "%s&lastObs=&from=&to=&"
            "filetype=csv&label=include&layout=seriescolumn" % maturity_map[m])

        name = '%i month T-Bill' % m
        df = pd.DataFrame.from_csv(url, header=5)
        df.columns = [name]
        big_df = big_df.append(df)

    return big_df.sort()

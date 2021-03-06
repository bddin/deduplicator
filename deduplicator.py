from string import punctuation

import redis
from simhash import Simhash


rds = redis.Redis(host='localhost', port=6379, db=0)  # noqa: WPS432


class Deduplicator():
    def preprocess(self, string):
        table = str.maketrans('', '', punctuation)
        list_string = string.translate(table).lower().split()
        list_string.sort()
        return ' '.join(list_string)

    def isduplicate(self, string):
        string = self.preprocess(string)
        hsh = Simhash(string).value
        if not rds.exists(hsh):
            rds.set(hsh, 1)
            return False
        return True

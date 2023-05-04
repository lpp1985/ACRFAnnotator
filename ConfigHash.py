#!/usr/bin/env python3
import re
from collections import defaultdict

class MultiRegexDict:
    def __init__(self):
        self._data = defaultdict(MultiRegexDict)
    
    def __getitem__(self, key):
        if key in self._data :
            return self._data[key]
        else:
            if isinstance(key, str):
                for k in self._data:
                    if isinstance(k,re.Pattern):
                        if k.findall( key ):
                            if isinstance(self._data[k],str):
                                if self._data[k].startswith("re#"):
                                    return k.sub( self._data[k].replace("re#",""),key)
                                else:
                                    return self._data[k]
                            else:

                                return self._data[k]
                else:
                    return self._data[key]
            else:
                return self._data[key]
            raise KeyError(key)
    
    def __setitem__(self, key, value):
        #if isinstance(key, str):
        self._data[key] = value

    def __repr__(self):
        return str(self._data)
    
    def __contains__(self, key):
        if isinstance(key, str):
            return key in self._data
        else:
            for k in self._data:
                if isinstance(k, tuple) and len(k) == len(key) and all(re.match(pattern, string) for pattern, string in zip(k, key)):
                    return True
            return False

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
# # code fot tsting
#
#
#
# md = MultiRegexDict()
# md["A"]["B"]["C"] = 123
# md["A"]["B"][re.compile("ABC\:(\d+)")] = 100
#
# md["A"]["B"][re.compile("CCD\:(\d+)")] = "re#\\1 LPP!!"
#
# print(md["A"]["B"]["C"]) # 123
# print(md["A"]["B"]["ABC:456"]) #100
# print(md["A"]["B"]["CCD:45123136"])
#  # 456
#print(md["A"]["B"][re.compile("ABC\:(\d+)")].group(1)) # 4151236
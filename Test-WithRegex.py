from collections import defaultdict
import re


class MultiRegexDict(defaultdict):
    def __init__(self):
        super().__init__(MultiRegexDict)
        self._data = set()
        self._subset = set()
        self._regex = ""
        self.k = ""  # a set for each dimension

    def __getitem__(self, key):

        if key in self:
            data = super().__getitem__(key)  # return a dict object
            data.k = key

            # print(key)
            return data  # return a dict object
        elif isinstance(key, str):
            for k in self:
                if isinstance(k, re.Pattern):
                    if k.findall(key):
                        data = self[k]
                        # print("Key is"+key)
                        # print("Key was "+self[k].k)
                        data.k = key
                        data._regex = k
                        return data
            else:
                data = super().__getitem__(key)
                data.k = key
            return data


        else:
            data = super().__getitem__(key)
            data.k = key
            return data

    def __setitem__(self, key, value):
        if isinstance(value, str):

            self.__getitem__(key)._data.add(value)
        elif isinstance(value, re.Pattern):
            self.__getitem__(key)._regex.add(value)
        elif isinstance(value, list):

            for v in value:

                if len(v) > 0:
                    self.__getitem__(key)._data.add(v)  # add string to set
        else:
            super().__setitem__(key, value)  # set value to Ddict object

    def data(self):
        return self._data  # return a set


x = MultiRegexDict()

# x["a"]["B"]
# x["aa"]["B"] = "hello"
x["a"]["B"]["D"] = ["world", "", "python"]
# x["a"]["B"]["D"] ="Data"

x["a"]["B"][re.compile("\d+")] = ["world111", "", "python"]
# print( x["a"]["B"] )
# print(x["a"]["B"]["D"].data())
print(x["a"]["B"]._regex,x["a"]["B"]["1"].k)
print(x["a"]["B"]["1"]._regex,x["a"]["B"]["1"].k)

from collections import defaultdict
import re
class MultiRegexDict(defaultdict):
    def __init__(self):
        super().__init__(MultiRegexDict)
        self._data = set() # a set for each dimension
    def __getitem__(self, key):
        if key in self:

            return super().__getitem__(key) # return a dict object
        elif  isinstance(key, str):
            for k in self:
                if isinstance(k, re.Pattern):
                    if k.findall(key):
                        return self[k]
            else:
                return super().__getitem__(key)


        else:
            return super().__getitem__(key)
    def __setitem__(self, key, value):
        if isinstance(value, str):
            # print("Data is "+value)
            # self.__getitem__(key)._data=set()
            self.__getitem__(key)._data.add(value)
            # print(self._data)# add string to set
        elif isinstance(value, list):
            # self.__getitem__(key)._data=set()
            for v in value:

                if len(v)>0 :
                    self.__getitem__(key)._data.add(v)  # add string to set
        else:
            super().__setitem__(key, value) # set value to Ddict object
    def data(self):
        return self._data # return a set
x = MultiRegexDict()

# x["a"]["B"]
x["aa"]["B"] = "hello"
x["a"]["B"]["D"] = ["world","", "python"]
x["a"]["B"]["D"] ="Data"

x["a"]["B"][re.compile("\d+")] = ["world111","", "python"]
# print( x["a"]["B"] )
print(x["a"]["B"]["D"].data())
print( x["a"]["B"].data() )
print(x["a"]["B"]["1"]["2"])
print(x["a"]["B"]["1"].data())


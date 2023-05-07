from collections import defaultdict
class Ddict(defaultdict):
    def __init__(self):
        super().__init__(Ddict)
        self._data = set() # a set for each dimension
    def __getitem__(self, key):
        return super().__getitem__(key) # return a Ddict object
    def __setitem__(self, key, value):
        if isinstance(value, str):
            # print("Data is "+value)
            self.__getitem__(key)._data=set()
            self.__getitem__(key)._data.add(value)
            # print(self._data)# add string to set
        elif isinstance(value, list):
            self._data = set()
            for v in value:

                if len(v)>0 :
                    self._data.add(v)  # add string to set
        else:
            super().__setitem__(key, value) # set value to Ddict object
    def data(self):
        return self._data # return a set
x = Ddict()
x["a"]["B"] = "hello"
# x["a"]["B"]["D"] = ["world", "python"]
print(x["a"]["B"].data()git
print(x["a"]["E"].data())
print(x["a"]["B"]["x"])

print(x["a"]["B"])

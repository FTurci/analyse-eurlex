import re
from collections import OrderedDict

class MyOrderedDict(OrderedDict):
    def last(self):
        key = next(reversed(self))
        return (key, self[key])

class LawParser():
    def __init__(self,path):
        self.path = path

    def parse_treaties(self):
        output = MyOrderedDict()
        with open(self.path) as fin:
            for line in fin:
                if 'Table of c'
                if 'TREATY' in line and 'class=\"bold\"' in line:
                    print(line)
                    output[line]={}
                if 'TITLE ' in line and 'tbl'  in line:
                    print("Line",line)
                    title = re.search(r'>(.*?|\n)</p>', line)
                    print(title)
                    last = output.last()
                    print(last)
        self.output= output



parser = LawParser('../ConsolidatedVersion.html')

parser.parse_treaties()
print (parser.output)
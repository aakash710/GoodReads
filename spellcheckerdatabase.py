import csv
import os
import sys
import re




'''
Strip invalid characters from the text.
'''
def strip_accents(string, accents=('COMBINING ACUTE ACCENT', 'COMBINING GRAVE ACCENT', 'COMBINING TILDE')):
    # accents = set(map(unicodedata.lookup, accents))
    # chars = [c for c in unicodedata.normalize('NFD', string) if c not in accents]
    return "".join(c for c in string if 63 < ord(c) < 123)

    # return unicode.unidecode(string)

directory = os.path.join(sys.path[0], 'bookdata')

spellcheckdict = dict()
import enchant
engdict = enchant.Dict("en_US") # get english dictionary

'''
It gets the csv row, and it creates alphabetical tokens which is then stored in dictionary.
It is used for spell check.
'''
def processrow(row, dictionary):
    tokens = []
    if row.get('Name') is not None:

        tokens += [strip_accents(word) for word in re.split(r'[\W+]|[-:.!~={}\\]]', row['Name']) if word != "" and engdict.check(word.lower())]
    if row.get('Authors') is not None:
        tokens += [strip_accents(word) for word in re.split(r'[\W+]|[-:.!~={}\\]]', row['Authors'])]
    # if row.get('Description') is not None:
    #     tokens += re.split(r'[\W+]|[-:.!~={}\\]]', row['Description'])
    for word in tokens:
        if len(word) > 1:
            newWord = "".join(e for e in word if e.isalpha()).lower()
            value = spellcheckdict.get(newWord)
            if value is not None:
                spellcheckdict[newWord] = value + 1
            else:
                spellcheckdict[newWord] = 1
    return spellcheckdict

#traversing through each csv to load the dictionary data.
for filename in os.listdir(directory):

    fullname = os.path.join(directory, filename)
    print(filename)
    if "book" in filename:
        with open(fullname, 'r', encoding='UTF-8') as file:
            bookDataList = []

            bookreader = csv.DictReader(file)
            lineCount = 0
            for row in bookreader:
                if lineCount == 0:
                    lineCount += 1

                else:
                    lineCount += 1
                    spellcheckdict = processrow(row, spellcheckdict)


import  json
spelldictd = open("./spelldictjson.json", "w")

data = json.dumps(spellcheckdict)
spelldictd.write(data)
spelldictd.close()


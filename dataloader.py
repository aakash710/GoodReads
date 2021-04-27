import csv
import os
import sys

directory = os.path.join(sys.path[0], 'bookdata')

'''
Creates index of elasticsearch based on names and properties
'''
def create_index(es, indexname):
    request_body = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "my_analyzer": {
                        "type": "standard",
                        "filter" : [
                            "lowercase",
                            "asciifolding",
                            "classic"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "id": { "type": "integer" },
                "ratingDistTotal": { "type": "integer"},
                "pagesNumber": { "type": "integer" },
                "publishDay": { "type": "integer" },
                "publishYear": { "type": "integer" },
                "publishMonth": { "type": "integer" },
                "rating": { "type": "integer" }
            }
        }
    }
    if es.indices.exists(indexname):
        print("deleting '%s' index..." % (indexname))
        res = es.indices.delete(index=indexname)
        print(" response: '%s'" % (res))
    print("creating '%s' index..." % (indexname))
    res = es.indices.create(index=indexname, body=request_body)
    print(" response: '%s'" % (res))

from elasticsearch import Elasticsearch, helpers
#connect to elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}], timeout=60, max_retries=10, retry_on_timeout=True)
# create index
create_index(es, "goodread")

import json

'''
Process csv row, extract respective fields and store them in a list of dictionaries. 
'''
def csvToDict(row):
    bookData = {}
    data = []
    if row is not None:
        if row.get('Id') is not None: bookData['id'] = row['Id']
        if row.get('Name') is not None:
            bookData['name'] = row['Name']
            # data += re.split(r'[\W+]|[-:.!~={}\\]]', row['Name'])
        if row.get('Description') is not None:
            bookData['description'] = row['Description']
            #data += re.split(r'[\W+]|[-:.!~={}\\]]', row['Description'])
        if row.get('RatingDist1') is not None: bookData['ratingDist1'] = row['RatingDist1'].split(":")[1]
        if row.get('pagesNumber') is not None: bookData['pagesNumber'] = row['pagesNumber']
        if row.get('RatingDist4') is not None: bookData['ratingDist4'] = row['RatingDist4'].split(":")[1]
        if row.get('RatingDistTotal') is not None: bookData['ratingDistTotal'] = row['RatingDistTotal'].split(":")[1]
        # else:
        #     bookData['ratingDistTotal'] = 0
        if row.get('PublishMonth') is not None: bookData['publishMonth'] = row['PublishMonth']
        if row.get('PublishDay') is not None: bookData['publishDay'] = row['PublishDay']
        if row.get('Publisher') is not None:
            bookData['publisher'] = row['Publisher']
            # data += re.split(r'[\W+]|[-:.!~={}\\]]', row['Publisher'])
        if row.get('CountsOfReview') is not None: bookData['countsOfReview'] = row['CountsOfReview']
        if row.get('PublishYear') is not None: bookData['publishYear'] = row['PublishYear']
        if row.get('Language') is not None: bookData['language'] = row['Language']
        if row.get('Authors') is not None:
            bookData['authors'] = row['Authors']
           # data += re.split(r'[\W+]|[-:.!~={}\\]]', row['Authors'])
        if row.get('Rating') is not None: bookData['rating'] = row['Rating']
        if row.get('RatingDist2') is not None: bookData['ratingDist2'] = row['RatingDist2'].split(":")[1]
        if row.get('RatingDist5') is not None: bookData['ratingDist5'] = row['RatingDist5'].split(":")[1]
        if row.get('ISBN') is not None: bookData['isbn'] = row['ISBN']
        if row.get('RatingDist3') is not None: bookData['ratingDist3'] = row['RatingDist3'].split(":")[1]

        return (bookData, data)

levenshtiendict = []

'''
Reading of files, extracting relevant csv, and processing their rows.
'''
for filename in os.listdir(directory):

    fullname = os.path.join(directory, filename)
    print(filename)
    if "book" in filename:
        with open(fullname, 'r', encoding='UTF-8') as file:
            bookDataList = []

            bookreader = csv.DictReader(file)
            bookData = {}
            lineCount = 0;
            for row in bookreader:
                if lineCount == 0:
                    lineCount += 1

                else:
                    lineCount += 1
                    # print(row['Id'])
                    # if lineCount > 900: #and lineCount < 1000 or lineCount > 570 and lineCount < 579:
                    #     continue
                    rowinDict = csvToDict(row)
                    # for token in rowinDict[1]:
                    #     if len(token) > 1:
                    #         if token.strip() not in levenshtiendict:
                    #             levenshtiendict.append(token.strip())
                    rowInJson = json.dumps(rowinDict[0])
                    bookDataList.append(rowInJson)
            helpers.bulk(es, bookDataList, index = "goodread")
#
# dict_eng = json.dumps({"id":1, "list":levenshtiendict})
# helpers.bulk(es, dict_eng, index = "spelldict")
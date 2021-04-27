import random
import math
import re
import matplotlib.pyplot as plt
import booksearch as bs
import csv
import os
import sys

directory = os.path.join(sys.path[0], 'bookdata')

from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

hits = dict()
nothits = dict()


def accuracy():
    count = 0
    randomSamples = es.search(index="goodread", body={"size": 10000, "sort": [{"_score": {"order": "desc"}}],
                                                      "query": {"range": {"id": {
                                                          "gte": random.randint(1, 300000),
                                                      }}, }})
    reviewcounter = dict()
    data = []
    hitfoundscounter = []
    for filename in os.listdir(directory):
        hits = dict()
        nothits = dict()
        fullname = os.path.join(directory, filename)
        print(filename)
        if "book" in filename:
            with open(fullname, 'r', encoding='UTF-8') as file:
                bookreader = csv.DictReader(file)

                for row in bookreader:
                    bookData = {}
                    if row is not None:
                        if row.get('Name') is not None:
                            bookData['name'] = row['Name'].strip()
                        if row.get('Authors') is not None:
                            bookData['authors'] = row['Authors'].strip()
                        ratingDistTotal = row.get('RatingDistTotal')
                        if ratingDistTotal is not None:
                            if reviewcounter.get(ratingDistTotal) is not None:
                                reviewcounter[ratingDistTotal] = reviewcounter[ratingDistTotal] + 1
                            else:
                                reviewcounter[ratingDistTotal] = 1
                    data.append(bookData)

        count = 0
        hitfoundscounter = []
        while (count < 1000):

            index = random.randint(0, len(data) - 1)
            searchdata = data[index]
            queryarray = searchdata['name'].split(" ")
            spliceInt = 1
            if len(queryarray) < 2:
                continue
            if len(queryarray) < 4:
                spliceInt = 1
            elif len(queryarray) < 5:
                spliceInt = 1
            elif len(queryarray) < 6:
                spliceInt = 2
            elif len(queryarray) < 7:
                spliceInt = 3
            elif len(queryarray) > 7:
                spliceInt = 4
            result = bs.book_search(" ".join(e for e in searchdata['name'].split(" ")[0:-spliceInt]).lower())[0:10]
            hitfoundat = 1
            for d in result:
                if d['name'].lower() == searchdata['name'].lower() and d['authors'].lower() == searchdata[
                    'authors'].lower():
                    hits[count] = (searchdata, d, hitfoundat)
                    hitfoundscounter.append(hitfoundat)
                    break
                hitfoundat += 1

            if hits.get(count) is None:
                nothits[count] = (searchdata, result)
            count += 1

        print("No of hits correct hits :" + str(len(hits)))
        print("No of hits incorrect hits :" + str(len(nothits)))
        # print(str(sum(hitfoundscounter)) + " " + str(len(hitfoundscounter) + (1000 - len(hitfoundscounter))))
        # plt.bar(hitfoundscounter, [0,1,2,3,4,5,6,7,8,9,10], color = 'maroon', width=0.4)
        # plt.show()

    # print(nothits)


#
#
# plt.bar(range(len(reviewcounter)), list(reviewcounter.values()), align='center')
# plt.xticks(range(len(reviewcounter)), list(reviewcounter.keys()))
# plt.show()
#
accuracy()

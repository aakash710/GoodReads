import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import sys
import re

directory = os.path.join(sys.path[0], 'bookdata')
totalReviewCount = dict()


def convertReviewToNormalized(reviewCount):
    if reviewCount < 100:
        return 100
    elif reviewCount < 200:
        return 200
    elif reviewCount < 300:
        return 300
    elif reviewCount < 400:
        return 400
    elif reviewCount < 500:
        return 500
    elif reviewCount < 1000:
        return 1000
    elif reviewCount < 2000:
        return 2000
    elif reviewCount < 3000:
        return 3000
    elif reviewCount < 4000:
        return 4000
    elif reviewCount < 5000:
        return 5000
    elif reviewCount < 6000:
        return 6000
    elif reviewCount < 7000:
        return 7000
    elif reviewCount < 8000:
        return 8000
    elif reviewCount < 9000:
        return 9000
    elif reviewCount < 10000:
        return 10000
    elif reviewCount < 11000:
        return 11000
    elif reviewCount < 12000:
        return 12000
    elif reviewCount < 13000:
        return 13000
    elif reviewCount < 14000:
        return 14000


def processrow(row, totalReviewCount):
    reviewCount = row.get('RatingDistTotal')
    if reviewCount is not None:
        reviewCount = reviewCount.split(":")[1]
        reviewCount = convertReviewToNormalized(int(reviewCount))

        if totalReviewCount.get(reviewCount) is not None:
            totalReviewCount[reviewCount] = totalReviewCount.get(reviewCount) + 1
        else:
            totalReviewCount[reviewCount] = 1
    return totalReviewCount

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
                    totalReviewCount = processrow(row, totalReviewCount)

colors = list("rgbcmyk")
normalizedreviews = dict()

# for key, value in totalReviewCount.items():
#     if int(value) > 1000:
#         normalizedreviews[convertReviewToNormalized(int(key))] = value

x = list(totalReviewCount.keys())
y = list(totalReviewCount.values())
# plt.scatter(x, y, color=colors.pop())
#
# plt.legend(totalReviewCount.keys())
# plt.show()

plt.bar(x, y)
plt.show()
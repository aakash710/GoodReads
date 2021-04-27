from flask import Flask, render_template, request

text = ""
suggestquery = ""
app = Flask(__name__, template_folder='template')

if __name__ == "__main__":
    app.run()

from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
authorUsed = False

'''
Loading spell check database and parameters settings. 
'''
from spellchecker import SpellChecker

spell = SpellChecker()
spell.word_frequency.load_dictionary('./spelldictjson.json')
spell.distance = 2

'''
Default search page link
'''
@app.route('/')
def start():
    return search()

'''
It takes the query given by the user, and based on commands, it finds the relevant document using ranking features
and once relevant documents are found, the data is sent to the view. It also creates suggested query which is used for 
spell correction. 
'''
@app.route('/search/res', methods=['POST'])
def my_new_search():
    text = str(request.form['input'])
    processedText = text.split("!a")[0]
    processedText = processedText.split("!p")[0]
    suggestions = dict()
    suggestquery = ""
    for word in spell.unknown(processedText.split(" ")):
        suggestions[word] = spell.correction(word)
    for word in text.split(" "):
        if len(word) > 1:
            if suggestions.get(word) is None:

                suggestquery += word + " "
            else:
                suggestquery += suggestions[word] + " "
    if suggestquery.lower().strip() == text.lower().strip():
        suggestquery = ""

    if "!a" in text:
        suggestquery = suggestquery.split(" a")[0]

    data = book_search(text)
    if (len(data) < 1):
        data = book_search(suggestquery + ("!a" if "!a" in text else "" + "!p" if "!p" in text else ""))
    queryData = {"text" : text, "suggestquery" : suggestquery}
    return render_template('Results.html', records=data, suggestquery=suggestquery, text=text, queryData = queryData)

'''
It is customized manual script scoring algorithm. It checks the ratings and uses log function to calculate the 
additional popularity score for each document. It uses minimum rating of 100 and multiples the output by 1. 
The factor can be increased from 1 to favor popular books. 
'''
def updateRankingBasedOnRatings(data, text):
    newData = []
    for d in data:
        if d['name'] == text:
            d['_score'] += 2
        d['_score'] = d['_score'] + math.log(d['totalRatings'] if d['totalRatings'] > 100 else 100 + 1) * 1
        newData.append(d)
    return newData

'''
Once a query is being processed, it is used here to get relevant query using match_phrase, multi_match
and/or exact field search. Depending on the search type. Once the documents are obtained from the search api,
a new ranking score is calculated based on above scoring function and the list is sorted based on the preference. 
'''
def book_search(text):
    data = dict()

    if "!a" in text:
        text = "".join(text.split("!a"))
        res = convertElasticDataToJson(searchBySpecificField(text, "authors", 20)) #search by just author
        for ad in res:
            data = addInResult(data, ad)
        if (len(data) < 1 and suggestquery != ""):
            data = book_search(suggestquery + " !a") #if no result found by author probably a typo

        data = updateRankingBasedOnRatings(data, text)

        data = sorted(data, key=lambda d: d.get('_score', 0), reverse=True) # sort data based on the score
        return data
    res = convertElasticDataToJson(searchByPhrase(text, count=10)) #data by exact search phrase of name field.

    newData = convertElasticDataToJson(searchByQueryPrefix(text, "name", 3)) #data by query prefix
    res += newData
    data = []
    for items in res:
        data = addInResult(data, items)
    if len(data) < 20:

        res2 = convertElasticDataToJson(searchByMultiMatch(text, count=20)) #get data by multimatch
        for ad in res2:
            data = addInResult(data, ad)
    data = updateRankingBasedOnRatings(data, text)
    data = sorted(data, key=lambda d: d.get('_score', 0), reverse=True)
    return data

'''
It uses Elasticsearch search API for specfic field search like name, author etc
'''
def searchBySpecificField(text, field, count):
    return es.search(index="goodread", body={"size": count, "sort": [{"_score": {"order": "desc"}}],
                                             "query": {"match": {
                                                 field: {
                                                     "query": text,
                                                     "analyzer": "my_analyzer"
                                                 }
                                             }}, })

'''
It checks for copies in the result. 
'''
def addInResult(data, input):
    if len(data) > 0:
        append = True
        for d in data:

            if d['name'].lower() == input['name'].lower() and d['authors'].lower() == input['authors'].lower():
                append = False
                if (d['_score'] < input['_score']): #assign better score obtained from different query api if the result is same
                    data.remove(d)
                    append = True
        if append: data.append(input)
        return data
    else:
        return [input]

'''
It uses Elasticsearch search API for multiple fields search like name, author etc
'''
def searchByMultiMatch(text, count):
    return es.search(index="goodread", body={"size": count, "sort": [{"_score": {"order": "desc"}}],
                                             "query": {"multi_match": {
                                                 "query": text,
                                                 "fields": ["name", "authors", "cescription"],
                                                 "analyzer": "my_analyzer"
                                             }},
                                             })

'''
It uses Elasticsearch search API for Name field only using exact phrase technique. 
'''
def searchByPhrase(text, count):
    return es.search(index="goodread", body={"size": count, "sort": [{"_score": {"order": "desc"}}],
                                             "query": {"match_phrase": {
                                                 "name": {
                                                     "query": text,
                                                     "analyzer": "my_analyzer"
                                                 }
                                             }}, })

'''
It uses Elasticsearch search API searching by prefix
'''
def searchByQueryPrefix(text, field, count):
    return es.search(index="goodread", body={"size": count, "sort": [{"_score": {"order": "desc"}}],
                                             "query": {"prefix": {
                                                 field : text
                                             }}, })

'''
Converts elastic data to json format.
'''
def convertElasticDataToJson(res):
    data = []
    for ad in res['hits']['hits']:
        dat = ad['_source']
        input = {'name': dat['name'].strip(),
                 'authors': dat['authors'].strip(),
                 'totalRatings': int(dat['ratingDistTotal']),
                 'description': dat.get('description'),
                 '_score': int(ad['_score'])}
        data.append(input)
    return data


import random
import math
import re

'''
default search redirect method
'''
@app.route('/search')
def search():
    return render_template('Upload2.html')

'''
Once Did you mean is clicked, it redirects here, and searches the documents based on correct spelling. 
'''
@app.route('/search/spellchecker')
def spellcheckapi():
    sug = request.args['suggestquery']

    sug += "!a" if "!a" in sug else ""
    data = book_search(sug)
    return render_template('Results.html', records=sorted(data, key=lambda d: d.get('_score', 0), reverse=True),
                           suggestquery="")


@app.route('/del')
def deletedoc():
    return es.delete_by_query(index='goodread', body={
        'query': {
            'match': {
                "id": "53708"
            }
        }
    })  #

# Goodread
GoodReads search engine using Python, Elasticsearch and SpellChecker

# Problem Statement <b>
I identified various issues in the GoodReads while exploring possible projects for the information retrieval course.
https://www.goodreads.com/

1. Search recommendation is inaccurate
2. Search Results are not relevant to user queries.
3. No spell correction feature. 

# Solution
I used Elasticsearch - an open source distributed search engine existing mapping and custom analyzer feature to tokenize the documents, lowercase the document, removing accents , and symbols between text using classic filter. 
Once the documents has been indexed, a spell correction database is created which is loaded in pyspellchecker to provide a spell correction functionality on the user query. 
Based on user query, the relevant documents are fetched using Elasticsearch search APIs like multi_match and match_phrase and the relevant documents are obtained from them.
Once the documents are obtained, extra scoring is added based on the popularity of the books. This helps in relevancy of the search engine. Script score is used for this where I am using Math.log to ensure highlypopular books don't skew the result.

# How to Run
1. Download Elasticsearch and Run elasticsearch.bat
2. Install flask, pyspellchecker, enchant, elasticsearch packages for python. 
3. Run python dataloader.py
4. Run python spellcheckerdatabase.py
5. Flask Run and use the following i.p to get the page. 127.0.0.1:5000

# Design Walk
`Dataloader.py` contains code for loading each csv and fetching their rows of books and storing them in the elasticsearch by bulk. Once all the information is stored in the elasticsearch, it ends.<br>
`Spellcheckerdatabase.py` It loads the rows from each of the csv tokenize the words and filters the text based only on a-z and A-Z. Once a custom dictionary is created it is stored in the `spelldictjson.json` <br>
`booksearch.py` contains the search ranking algorithm and the flask API for searching and spell correction. It also contains script_score formula along with tuning parameters. <br>
`template` folder contains html files and css files.<br>

# Resources Used
https://www.elastic.co/guide/en/elasticsearch/guide/current <br>
https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-script-score-query.html#field-value-factor <br>
https://www.stackoverflow.com <br>
https://www.kaggle.com/bahramjannesarr/goodreads-book-datasets-10m

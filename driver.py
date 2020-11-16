import sys
sys.path.insert(1, './src')
from searchEngine import SearchEngine
from readData import getSnippets

from elasticsearch import helpers, Elasticsearch
import csv
import os
import json
import time

def genData(snippets, filename):
    for row, snippet in enumerate(snippets):
        yield {
            "_index": "news_prog",
            "id": (filename, row + 2),
            "snippet": snippet
        }

if __name__ == "__main__":
    dirPath = os.path.dirname(os.path.realpath(__file__))
    dataPath = os.path.realpath(os.path.join(dirPath, "data"))
    files = [os.path.join(dataPath, file)
                for file in sorted(os.listdir(dataPath))]

    # Our Search Engine
    engine = SearchEngine()

    # Elasticsearch
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    for file in files:
        snippets = getSnippets(file)
        filename = int(os.path.split(file)[1].split(".csv")[0])
        helpers.bulk(es, genData(snippets, filename))

    while True:

        print("\n\n0. Standard query")
        print("1. Allows positional indexing")
        print("2. Allows wildcard terms")
        print("3. Allows both wildcards and positional indexing")
        print("Type a query and mention the type of query. Ex - \"0, Standard query\" ")
        print("Ctrl + D to exit")

        queryType, query = [w.strip() for w in input().split(',')]

        start = time.time()
        res = engine.search(query, int(queryType))
        end = time.time()

        modified_output = {"took": end - start, "total": len(res), "hits": []}
        for doc_q in res:
            for doc in doc_q:
                res_file = os.path.join(dataPath, str(doc[0][0]) + ".csv")
                with open(res_file) as fd:
                    reader = csv.DictReader(fd)
                    
                    row_no = 0
                    for row in reader:
                        if row_no == doc[0][1] - 2:
                            current_row = row
                            break
                        row_no += 1

                    modified_output["hits"].append({**{"id": doc[0]}, **{"score": doc[1]}, **current_row})
        print(json.dumps(modified_output, indent=1))
                
        if queryType == 0:
            query_body = {
                "query": {
                    "match": {
                        "snippet": query
                    }
                }
            }
            result = es.search(index="news_prog", body=query_body)

            es_docs = []
            for doc in result["hits"]["hits"]:
                es_docs.append(doc["_source"]["id"])
            
            correct_docs = 0
            for doc, row in res:
                if [doc, row] in es_docs:
                    correct_docs += 1
            
            precision = correct_docs / len(res)
            print("\nPrecision = ", precision)
    

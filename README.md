# Search-Engine
A simple search engine which uses the environmental news dataset as its corpus.

The Search engine performs pre-processing of query terms removing stop words, and performing lemmatization to normalize the terms.   

The search engine supports the following queries:
 1. bag of words unions and intersection
 2. positional queries
 3. wildcard queries
 4. combination of these queries 

The search engine ranks the documents using a vector-space model. 

## Setup and Execution

-   The dataset can be found [here](https://www.kaggle.com/amritvirsinghx/environmental-news-nlp-dataset), but has already been added to the project for convinence. 
-   Run `pip install -r requirements.txt`
-   Run `python3 driver.py` to start the search engine.

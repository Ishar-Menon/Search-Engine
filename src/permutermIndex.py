import os
import itertools
import pickle
import sys
from BTrees.OOBTree import OOBTree as BTree
from collections import defaultdict


def rotate(word):
    word = word[-1] + word[:-1]
    return word


def rotateWord(word):
    words = []
    word += "{"
    for i in range(len(word)):
        word = rotate(word)
        words.append(word)

    return words


def rotateQuery(query):
    q = query.split("*")

    if len(q) > 2 or len(q) == 1:   # zero or multiple *s not supported
        queryMin, queryMax = "", ""
    elif q[0] == "":                # *X => *X$ => X$*
        queryMin = q[1] + "{"
        queryMax = queryMin.replace("{", "}")
    elif q[1] == "":                # X* => X*$ => $X*
        queryMin = "{" + q[0]
        queryMax = "{" + q[0][:-1] + chr(ord(q[0][-1]) + 1)
    else:                           # X*Y => X*Y$ => Y$X*
        queryMin = q[1] + "{" + q[0]
        queryMax = q[1] + "{" + q[0][:-1] + chr(ord(q[0][-1]) + 1)

    return queryMin, queryMax


class PermutermIndex:
    def __init__(self, invertedIndex):
        self._invertedIndex = invertedIndex
        self._btree = BTree()
        self.build()

    def build(self):
        """ 
            Reads words in invertedIndex and builds and permutermIndex

            Arguments:
            None

            Returns:
            None
        """
        if os.path.isfile("PermutermIndex"):
            print("Loading the Permuterm Index from file")
            with open("PermutermIndex", "rb") as file:
                self._btree = pickle.load(file)
        else:
            print("Building the Permuterm Index")

            words = self._invertedIndex.getKeys()

            for word in words:
                wordsRotated = rotateWord(word)
                for wordR in wordsRotated:
                    self._btree.insert(wordR, word)

            sys.setrecursionlimit(100000)
            with open("PermutermIndex", "wb") as file:
                print("Saving the Permuterm Index to file")
                pickle.dump(self._btree, file)

    def search(self, query):
        """
            Searches the permuterm index for the wildcard query

            Arguments:
            query - wildcard query to search the permuterm index

            Returns:
            List of words matching the query
        """
        queryMin, queryMax = rotateQuery(query)
        if queryMin == "":
            return []

        matches = set()
        for word in self._btree.keys(queryMin, queryMax):
            if word == queryMax:
                break
            actualWord = self._btree.get(word)
            matches.add(actualWord)

        matches = list(matches)
        return matches

    def getDocuments(self, termList, queryType=0, queryMetadata=defaultdict(int)):
        """
            Finds the documents containing the terms

            Arguments:
            termList - List of query terms

            Returns:
            List of document numbers
        """
        if queryType == 2:
            queryType = 0
        elif queryType == 3:
            queryType = 1

        allTerms = []
        for term in termList:
            if "*" in term:
                res = self.search(term)
            else:
                res = [term]
            if res != []:
                allTerms.append(res)

        termList = list(itertools.product(*allTerms))
        docList = [(self._invertedIndex.getDocuments(doc, queryType, queryMetadata), doc)
                   for doc in termList]
        docList = [doc for doc in docList if doc[0] != []]
        return docList

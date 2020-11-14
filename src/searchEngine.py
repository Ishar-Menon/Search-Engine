import os
from preProcess import preProcess
from inverterdIndex import InvertedIndex
from vectorSpace import VectorSpace
from output import generateOutput
from permutermIndex import PermutermIndex


class SearchEngine:

    def __init__(self):
        super().__init__()
        self._index = InvertedIndex()
        self._vectorSpace = VectorSpace(self._index)
        self._permutermIndex = PermutermIndex(self._index)

    def search(self, query):
        """
            Searches the IR system for relavent documets

            Arguments:
            query - string query

            Returns:
            JSON formatted documet output
        """

        if "*" in query:
            termList = query.split(" ")
            docs = self._permutermIndex.getDocuments(termList)
            rankedDocList = []

            for docList, termList in docs:
                rdl = self._vectorSpace.vectorSpaceRank(
                    docList, termList)
                rankedDocList.append(rdl)

        else:
            termList = preProcess(query, True)
            docList = self._index.getDocuments(termList)
            rankedDocList = self._vectorSpace.vectorSpaceRank(
                docList, termList)

        #output = generateOutput(rankedDocList)
        return rankedDocList

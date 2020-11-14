import os
from preProcess import preProcess
from inverterdIndex import InvertedIndex
from vectorSpace import VectorSpace
from output import generateOutput


class SearchEngine:

    def __init__(self):
        super().__init__()
        self._index = InvertedIndex()
        self._vectorSpace = VectorSpace(self._index)

    def search(self, query):
        """
            Searches the IR system for relavent documets

            Arguments:
            query - string query

            Returns:
            JSON formatted documet output
        """

        termList = preProcess(query, True)
        print(termList)
        queryMetadata = {(0,1) : 2, (1,2) : 4, (2,3) : 2}
        docList = self._index.getDocuments(termList,1,queryMetadata)
        print(len(docList))
        rankedDocList = self._vectorSpace.vectorSpaceRank(docList,termList)
        #output = generateOutput(rankedDocList)
        return rankedDocList

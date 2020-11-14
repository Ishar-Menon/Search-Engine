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

    def search(self, query, queryType):
        """
            Searches the IR system for relevant documents

            Arguments:
            query - String query

            Returns:
            JSON formatted document output
        """

        termList, queryMetadata = preProcess(query, True, queryType)
        print(termList)
        docList = self._index.getDocuments(termList, queryType, queryMetadata)
        print(len(docList))
        rankedDocList = self._vectorSpace.vectorSpaceRank(docList, termList)
        #output = generateOutput(rankedDocList)
        return rankedDocList

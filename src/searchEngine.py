import os
from preProcess import preProcess
from inverterdIndex import InvertedIndex
from permutermIndex import PermutermIndex
from vectorSpace import VectorSpace
from output import generateOutput


class SearchEngine:

    def __init__(self):
        super().__init__()
        self._index = InvertedIndex()
        self._vectorSpace = VectorSpace(self._index)
        self._permutermIndex = PermutermIndex(self._index)

    def search(self, query, queryType):
        """
            Searches the IR system for relevant documents

            Arguments:
            query - String query

            Returns:
            JSON formatted document output
        """

        if queryType < 2:
            termList, queryMetadata = preProcess(query, queryType)
            # print(termList, queryMetadata)
            docList = self._index.getDocuments(
                termList, queryType, queryMetadata)
            # print(len(docList))
            rankedDocList = self._vectorSpace.vectorSpaceRank(
                docList, termList)
            #output = generateOutput(rankedDocList)

        else:
            termList, queryMetadata = preProcess(query, queryType)
            docs = self._permutermIndex.getDocuments(
                termList, queryType, queryMetadata)

            rankedDocList = []
            for docList, termList in docs:
                rdl = self._vectorSpace.vectorSpaceRank(
                    docList, termList)
                rankedDocList.append(rdl)
            #output = generateOutput(rankedDocList)

        return rankedDocList

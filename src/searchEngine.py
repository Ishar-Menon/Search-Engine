import os
from preProcess import preProcess
from inverterdIndex import InvertedIndex
from vectorSpace import vectorSpaceRank
from output import generateOutput
from readData import getSnippets


class SearchEngine:

    def __init__(self):
        super().__init__()
        self._index = InvertedIndex()

    def build(self):
        """ 
            Reads files one-by-one and builds the index

            Arguments:
            None

            Returns:
            None
        """

        dirPath = os.path.dirname(os.path.realpath(__file__))
        dataPath = os.path.realpath(os.path.join(dirPath, "..", "data"))
        files = [os.path.join(dataPath, file)
                 for file in sorted(os.listdir(dataPath))]

        for file in files:
            snippets = getSnippets(file)
            for index, snippet in enumerate(snippets):
                filename = os.path.split(file)[1]
                docId = f"{filename}_{index+2}"

                termList = preProcess(snippet)
                self._index.updateIndex(termList, docId)

    def search(self, query):
        """
            Searches the IR system for relavent documets

            Arguments:
            query - string query

            Returns:
            JSON formatted documet output
        """

        termList = preProcess(query)

        docList = self._index.getDocuments(termList)

        rankedDocList = vectorSpaceRank(docList)

        output = generateOutput(rankedDocList)

        return docList

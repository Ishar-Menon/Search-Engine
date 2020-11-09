from preProcess import preProcess
from inverterdIndex import InvertedIndex
from vectorSpace import vectorSpaceRank
from output import generateOutput

class Main:

    def __init__(self):
        super().__init__()
        self.invertedIndex =  InvertedIndex()

    def search(self, query):
        """
            Searches the IR system for relavent documets

            Arguments:
            query - string query
        
            Returns:
            JSON formatted documet output
        """
        
        termList = preProcess(query)

        docList = self.invertedIndex.getDocuments(termList)

        rankedDocList = vectorSpaceRank(docList)

        output = generateOutput(rankedDocList)

        return output


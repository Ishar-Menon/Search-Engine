import os
from BTrees.OOBTree import OOBTree as BTree
from preProcess import preProcess
from readData import getSnippets


class InvertedIndex:
    def __init__(self):
        super().__init__()
        self._btree = BTree()
        self.build()

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

                tokens = preProcess(snippet)
                self.updateIndex(tokens, docId)

    def getDocuments(self, termList):
        """
            Finds the documents containing the terms

            Arguments:
            termList - List of query terms

            Returns:
            List of document numbers
        """

        result = []

        for term in termList:
            postingList = self._btree.get(term)
            result.append(postingList)

        return result

    def updateIndex(self, docTokens, docId):
        """
            Updates the inverted index

            Arguments:
            docText - Document to be added to the index
            docId - ID of the document

            Returns:
            None
        """

        for word, wordIndex in docTokens:
            postingList = self._btree.get(word)
            if postingList is not None:
                lastdocId = postingList[-1][0]
                if docId == lastdocId:
                    postingList[-1][1].append(wordIndex)
                else:
                    postingList.append((docId, [wordIndex]))
            else:
                postingList = [(docId, [wordIndex])]
                self._btree.insert(word, postingList)

from BTrees.OOBTree import OOBTree as BTree


class InvertedIndex:
    def __init__(self):
        super().__init__()
        self._btree = BTree()

    def getDocuments(self, termList):
        """
            Finds the documents containing the terms

            Arguments:
            termList - List of query terms

            Returns:
            List of document numbers
        """

        termList = termList.split(" ") if type(termList) == str else termList
        result = []

        for term in termList:
            postingList = self._btree.get(term)
            result.append(postingList)

        return result

    def updateIndex(self, docText, docId):
        """
            Updates the inverted index

            Arguments:
            docText - Document to be added to the index
            docId - ID of the document

            Returns:
            None
        """

        docWords = docText.split(" ") if type(docText) == str else docText

        for wordIndex, word in enumerate(docWords):
            postingList = self._btree.get(word)
            if postingList is not None:
                docIds = [doc[0] for doc in postingList]
                if docId in docIds:
                    docIdIndex = docIds.index(docId)
                    postingList[docIdIndex][1].append(wordIndex)
                else:
                    postingList.append((docId, [wordIndex]))
            else:
                postingList = [(docId, [wordIndex])]
                self._btree.insert(word, postingList)

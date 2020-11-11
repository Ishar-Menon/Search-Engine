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
                docIds = [doc[0] for doc in postingList]
                if docId in docIds:
                    docIdIndex = docIds.index(docId)
                    postingList[docIdIndex][1].append(wordIndex)
                else:
                    postingList.append((docId, [wordIndex]))
            else:
                postingList = [(docId, [wordIndex])]
                self._btree.insert(word, postingList)

        # for word, wordIndex in docTokens:
        #     postingList = self._btree.get(word)
        #     if postingList is not None:
        #         if docId in postingList:
        #             postingList[docId].append(wordIndex)
        #         else:
        #             postingList[docId] = [wordIndex]
        #     else:
        #         postingList = {docId: [wordIndex]}
        #         self._btree.insert(word, postingList)

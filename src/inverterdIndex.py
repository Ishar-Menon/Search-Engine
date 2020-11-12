import os
import pickle
import sys
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
        try:
            fh = open ("Btree.txt", "rb")
            self._btree = pickle.load(fh)

        except FileNotFoundError:
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

            sys.setrecursionlimit(10000)

            with open("Btree.txt", 'wb') as fh:
                pickle.dump(self._btree, fh)

    def getKeys(self):
        return self._btree.keys()

    def getValues(self):
        return self._btree.values()
        

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
            if(postingList != None):
                result.append(postingList)
            else:
                result.append([])

        docList = self.documentIntersection(result)
        return docList

    def documentIntersection(self,documents):

            #print(documents)
            documents.sort(key = lambda x : len(x), reverse = True)

            while(len(documents) > 1):
                list1 = documents.pop()
                list2 = documents.pop()

                ptr1 = 0
                ptr2 = 0
                
                intersection = []

                while(ptr1 < len(list1) and ptr2 < len(list2)):
                    elem1 = int(list1[ptr1][0].split('_')[1])
                    elem2 = int(list2[ptr2][0].split('_')[1])

                    if(elem1 == elem2):
                        intersection.append((list1[ptr1][0], []))
                        ptr1 += 1
                        ptr2 += 1
                    elif(elem1 < elem2):
                        ptr1 += 1
                    else:
                        ptr2 += 1

                documents.append(intersection)
            
            docNolist = [x[0] for x in documents[0]]
            return docNolist

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

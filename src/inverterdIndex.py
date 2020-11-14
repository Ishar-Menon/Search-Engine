import os
import pickle
import sys
from BTrees.OOBTree import OOBTree as BTree
from preProcess import preProcess
from readData import getSnippets
from collections import defaultdict

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
                    filename = int(os.path.split(file)[1].split(".csv")[0])
                    docId = (filename,index+2)
                    tokens = preProcess(snippet)
                    self.updateIndex(tokens, docId)

            self.sortPostingLists()

            sys.setrecursionlimit(10000)

            with open("Btree.txt", 'wb') as fh:
                pickle.dump(self._btree, fh)

    def sortPostingLists(self):
        words = list(self.getKeys())
        
        for word in words:
            postingList = self._btree.get(word)
            postingList.sort( key = lambda x : ( (10000*x[0][0]) +  x[0][1] ) )

    def getKeys(self):
        return self._btree.keys()

    def getValues(self):
        return self._btree.values()
        

    def getPostingListCollection(self, termList):

        result = []

        for term in termList:
            postingList = self._btree.get(term)
            if(postingList != None):
                result.append(postingList)
            else:
                result.append([])

        return result

    def getwildcardMatchedTerms(self, wildcardTerm):
        pass

    def wildCardPostingList(self, wildcardTerm):
        
        terms = getwildcardMatchedTerms(wildcardTerm)
        postingListCollection = getPostingListCollection(terms)
        merged = defaultdict(int)
        for postingList in postingListCollection:
            for doc in postingList:
                if(merged[doc[0]] == 0):
                     merged[doc[0]] = doc[1]
                else:
                    merged[doc[0]] = merged[doc[0]] + doc[1]
        
        mergedPostingList = []
        for docNo in merged:
            merged[docNo].sort()
            mergedPostingList.append((docNo,merged[docNo]))

        return mergedPostingList 

    def wildcardQueryPostingListCollection(self, termList, queryMetadata):
        
        postingListCollection = []

        for index,term in enumerate(termList):
            if(queryMetadata[index] == 1) :
                postingList = self.wildCardPostingList(term)
            else :
                postingList = self._btree.get(term)
                if(postingList == None):
                    postingList = []
            postingListCollection.append(postingList)

    def documentUnion(self,postingListCollection):
        docList = set()
        for postingList in postingListCollection:
            for doc in postingList:
                docList.add(doc[0])
            
        return docList

    def getDocuments(self, termList, queryType = 0, queryMetadata = defaultdict(int)):
        """
            Finds the documents containing the terms

            Arguments:
            termList - List of query terms

            Returns:
            List of document numbers
        """
        docList = []

        # Union
        if(queryType == 0):
            postingListCollection = self.getPostingListCollection(termList)
            docList =  self.documentUnion(postingListCollection)

        # intersection/positional
        elif(queryType == 1):
            postingListCollection = self.getPostingListCollection(termList)
            docList = self.documentIntersection(postingListCollection, queryMetadata)

        # wildcard - union
        elif(queryType == 2):
            postingListCollection = self.wildcardQueryPostingListCollection(termList, queryMetadata)
            docList = self.documentUnion(postingListCollection)
        
        # wildcard - intersection/positional
        elif(queryType == 3):
            postingListCollection = self.wildcardQueryPostingListCollection(termList, queryMetadata)
            docList = self.documentIntersection(postingListCollection)

        return docList

    def documentIntersection(self,documents, queryMetadata):

            while(len(documents) > 1):
                isPositional = False
                diff = queryMetadata[(len(documents) - 2,len(documents) - 1)] 
                if( diff != 0):
                    isPositional = True

                list1 = documents.pop()
                list2 = documents.pop()

                ptr1 = 0
                ptr2 = 0
                
                intersection = []

                while(ptr1 < len(list1) and ptr2 < len(list2)):

                    fileNo1 = list1[ptr1][0][0]
                    rowNo1 = list1[ptr1][0][1]
                    fileNo2 = list2[ptr2][0][0]
                    rowNo2 = list2[ptr2][0][1]

                    if(fileNo1 == fileNo2 and rowNo1 == rowNo2):
                        if(isPositional) :
                            for postion1 in list1[ptr1][1]:
                                for postion2 in list2[ptr2][1]:
                                    if((postion1 - postion2 + 1)  == diff):
                                        if(len(intersection) == 0 or intersection[-1][0] != list1[ptr1][0]):
                                            intersection.append((list1[ptr1][0], [postion2]))
                                        elif(intersection[-1][0] == list1[ptr1][0]):
                                            intersection[-1][1].append(postion2)
                        else :
                            intersection.append((list1[ptr1][0], list2[ptr2][1]))
                        ptr1 += 1
                        ptr2 += 1
                    elif(fileNo1 == fileNo2 and rowNo1 < rowNo2):
                        ptr1 += 1
                    elif(fileNo1 == fileNo2 and rowNo1 > rowNo2):
                        ptr2 += 1
                    elif(fileNo1 < fileNo2):
                        ptr1 += 1
                    elif(fileNo1 > fileNo2):
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

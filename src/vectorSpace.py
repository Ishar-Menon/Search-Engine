import math

def normalize(vectors):
    denominator = 0
    for values in vectors:
        temp = values*values
        denominator=denominator+ temp
    denominator= math.sqrt(denominator)
    for var in range(len(vectors)):
        vectors[var]=vectors[var]/denominator
    return vectors


class VectorSpace:
    def __init__(self,_index):
        super().__init__()
        self.N = 94858
        self.docVectors ={}
        self.wordIndex ={}
        self.i=-1
        self.buildVector(_index)
    
    def buildVector(self,_index):
        print("starting")
        terms = list(_index.getKeys())
        self.totalTerms = len(terms)
        #print(self.totalTerms)
        termValues = list(_index.getValues())
        for word,postingList in zip(terms,termValues):
            numDocs = len(postingList)
            ratioOfDocs = self.N / numDocs
            #print(ratioOfDocs)
            idf = math.log10(ratioOfDocs)
            self.i=self.i+1
            for docTuple in postingList:
                freq = len(docTuple[1])
                tf = 1+(math.log10(freq))
                documentNo = docTuple[0]
                if documentNo in self.docVectors:
                    self.docVectors[documentNo].append((self.i,tf*idf))
                else:
                    self.docVectors[documentNo]=[]
                    self.docVectors[documentNo].append((self.i,tf*idf))
        
            #print(self.i," ",idf)
            self.wordIndex[word]=(self.i,idf)
        print("ending")    


    def dotProduct(self,vector1,vector2):
        score=0
        for value1,value2 in zip(vector1,vector2):
            scoreOnIndiviualAxis = value1*value2
            score=score + scoreOnIndiviualAxis
        return score


    def getDocVector(self,docList):
        docVector = [0]*self.totalTerms
        for tempTuple in docList:
            docVector[tempTuple[0]]=tempTuple[1]
        docVector=normalize(docVector)
        return docVector


    def vectorSpaceRank(self,documents,query):
        """
        ranks the documents
        Arguments:
        docList - List of docments numbers
        
        Returns:
        Ranked list of document numbers
        """
        queryVector = self.getQueryVector(query)
        rankList = []
        for doc in documents:
            docList = self.docVectors[doc]
            docVector = self.getDocVector(docList)
            score = self.dotProduct(docVector,queryVector)
            scoreDocumentTuple = (score,doc)
            rankList.append(scoreDocumentTuple)
        rankList.sort(key = lambda x: x[0],reverse=True)
        rankedDocuments = []
        for scoreDoc in rankList:
            rankedDocuments.append(scoreDoc[1])
        return rankedDocuments


    def getQueryVector(self,query):
        queryCount = {} 
        for word in query:
            if word in queryCount:
                queryCount[word]=queryCount[word]+1
            else:
                queryCount[word]=1
        
        queryVector =[0]*self.totalTerms
        for word in queryCount:
            index = self.wordIndex[word][0]
            idf = self.wordIndex[word][1]
            freq = queryCount[word]
            tf = 1+(math.log10(freq))
            value = tf*idf
            queryVector[index]=value
        
        queryVector = normalize(queryVector)
        return queryVector
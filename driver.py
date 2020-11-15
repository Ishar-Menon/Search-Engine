import sys
sys.path.insert(1, './src')
from searchEngine import SearchEngine

if __name__ == "__main__":
    engine = SearchEngine()

    query = "another /2 billion /4 half /2 people"
    res = engine.search(query, 1)
    print(res)

    #query = "liverpool city"
    #res = engine.search(query,0)
    #print(f"res: {res}")

    #query = "l*pool city"
    #res = engine.search(query,2)
    #print(f"res: {res}")


    #query = "l*pool /3 city"
    #res = engine.search(query,3)
    #print(f"res: {res}")

    query = "liverpool /3 city"
    res = engine.search(query,1)
    print(f"res: {res}")
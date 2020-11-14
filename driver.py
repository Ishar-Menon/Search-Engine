import sys
sys.path.insert(1, './src')
from searchEngine import SearchEngine

if __name__ == "__main__":
    engine = SearchEngine()

    # query = "another billion and a half people"
    # res = engine.search(query)
    # print(res)

    query = "l*pool ci*y"
    res = engine.search(query)
    print(res)

    query = "liverpool city"
    res = engine.search(query)
    print(res)

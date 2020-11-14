import sys
sys.path.insert(1, './src')
from searchEngine import SearchEngine

if __name__ == "__main__":
    engine = SearchEngine()

    query = "the usa continues to review its policy and donald trump himself is tweeted"
    res = engine.search(query)
    print(res)
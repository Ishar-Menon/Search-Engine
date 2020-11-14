import sys
sys.path.insert(1, './src')
from searchEngine import SearchEngine

if __name__ == "__main__":
    engine = SearchEngine()

    query = "another /2 billion /4 half /2 people"
    res = engine.search(query, 1)
    print(res)
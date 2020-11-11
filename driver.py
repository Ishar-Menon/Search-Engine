import sys
sys.path.insert(1, './src')
from searchEngine import SearchEngine

if __name__ == "__main__":
    engine = SearchEngine()
    engine.build()

    query = "office"
    res = engine.search(query)
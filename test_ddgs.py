yupefrom duckduckgo_search import DDGS
import json

def test():
    query = 'site:linkedin.com/in "Software Engineer" "Google" "IIT Madras"'
    print("Testing query:", query)
    try:
        ddgs = DDGS()
        results = ddgs.text(query, max_results=5)
        print("Results:")
        print(json.dumps(results, indent=2))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test()

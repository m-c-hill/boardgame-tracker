def test_search_returns_results_with_search_term(client):
    client.post("/api/search", json={"search_term": "wingspan"})

def test_search_returns_results_with_no_search_term(client):
    client.post("/api/search")
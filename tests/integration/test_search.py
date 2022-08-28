def test_search_returns_results_with_search_term(client, search_results):
    response = client.post("/api/search", json={"search_term": "wingspan"})
    assert response.status_code == 200
    assert response.get_json() == search_results

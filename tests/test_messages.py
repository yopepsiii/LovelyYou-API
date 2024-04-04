def test_get_all_messages(authorized_client):
    res = authorized_client.get('/messages/')
    print(res.json())
    assert res.status_code == 200

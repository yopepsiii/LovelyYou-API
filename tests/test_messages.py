def test_get_all_messages(authorized_client, test_messages):
    res = authorized_client.get('/messages/')

    def validate(message):
        pass # Доделать
    print(res.json())
    assert res.status_code == 200

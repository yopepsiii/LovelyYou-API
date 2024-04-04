from app.schemas import message as message_schemas
from app.schemas import user as user_schemas


def test_get_all_messages(authorized_client, test_messages):
    res = authorized_client.get('/messages/')
    print(res.json())

    def validate(message):
        return message_schemas.Message(**message)

    messages = list(map(validate, res.json()))

    print(messages)
    assert res.status_code == 200
    assert len(messages) == len(test_messages)


def test_unauthorized_get_all_messages(client):
    client.headers.__delitem__('Authorization')
    res = client.get('/messages/')
    print(res.json())
    print(client.headers)
    assert res.status_code == 401


def test_get_one_message(authorized_client, test_messages):
    res = authorized_client.get(f'/messages/{test_messages[0].id}')
    print(res.json())

    message = message_schemas.Message(**res.json())

    assert res.status_code == 200
    assert message.id == test_messages[0].id


def test_get_one_unexisting_message(authorized_client):
    res = authorized_client.get(f'/messages/{99999}')
    assert res.status_code == 404


def test_update_message(authorized_client, test_messages):
    res = authorized_client.put(f'/messages/{test_messages[0].id}', json={'title': 'New title', 'content': 'New content'})
    print(res.headers.get('Authorization'))
    assert res.status_code == 200
    assert res.json().get('title') == 'New title'
    assert res.json().get('content') == 'New content'


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

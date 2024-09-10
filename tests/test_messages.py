import pytest

from app.schemas import message as message_schemas
from app.schemas import user as user_schemas


# GET MESSAGE
def test_get_all_messages(authorized_client, test_messages):
    res = authorized_client.get("/messages/")

    def validate(message):
        return message_schemas.Message(**message)

    messages = list(map(validate, res.json()))

    print(messages)
    assert res.status_code == 200
    assert len(messages) == len(test_messages)


def test_get_my_messages(authorized_client, test_messages):
    res = authorized_client.get("/messages/for_me/")

    def validate(message):
        return message_schemas.Message(**message)

    my_messages = list(map(validate, res.json()))
    print(my_messages)

    assert res.status_code == 200
    assert my_messages[0].creator.id == my_messages[len(my_messages) - 1].creator.id


def test_unauthorized_get_all_messages(client):
    res = client.get("/messages/")
    print(res.json())
    print(client.headers)
    assert res.status_code == 401


def test_get_one_message(authorized_client, test_messages):
    res = authorized_client.get(f"/messages/{test_messages[0].id}")
    print(res.json())

    message = message_schemas.Message(**res.json())

    assert res.status_code == 200
    assert message.id == test_messages[0].id


def test_get_one_unexisting_message(authorized_client):
    res = authorized_client.get(f"/messages/999999")
    assert res.status_code == 404


# UPDATE MESSAGE
def test_update_message(authorized_client, test_messages, test_updated_data):
    res = authorized_client.put(
        f"/messages/{test_messages[0].id}", json=test_updated_data
    )
    updated_message = message_schemas.MessageUpdate(**res.json())
    print(updated_message.json())
    assert res.status_code == 200
    assert updated_message.title == test_updated_data["title"]
    assert updated_message.content == test_updated_data["content"]


def test_update_message_of_other_user(
    authorized_client, test_messages, test_updated_data
):
    res = authorized_client.put(
        f"/messages/{test_messages[2].id}", json=test_updated_data
    )
    assert res.status_code == 403


def test_update_message_unauthorized(client, test_messages, test_updated_data):
    res = client.put(f"/messages/{test_messages[0].id}", json=test_updated_data)
    assert res.status_code == 401


def test_update_unexisting_message(authorized_client, test_updated_data):
    res = authorized_client.put("/messages/99999999", json=test_updated_data)
    assert res.status_code == 404


# DELETE MESSAGE


def test_delete_message(authorized_client, test_messages):
    res = authorized_client.delete(f"/messages/{test_messages[0].id}")
    assert res.status_code == 204


def test_delete_message_of_other_user(authorized_client, test_messages):
    res = authorized_client.delete(f"/messages/{test_messages[2].id}")
    assert res.status_code == 403


def test_delete_unexisting_message(authorized_client, test_messages):
    res = authorized_client.delete("/messages/9999999")
    assert res.status_code == 404


# CREATE MESSAGE
@pytest.mark.parametrize(
    "title, content, receiver_id, status_code",
    [
        ("Новый пепси", "Ну как новый, просто старый", 2, 201),
        ("Новый пепси", "Ну как новый, просто старый", 1, 201),
        ("Люблю пиццу", None, 2, 422),
        (None, "но без мацареллы", 2, 422),
        (None, None, 2, 422),
        ("Бесподобно", "Очень даже!", None, 422),
        (None, None, None, 422),
    ],
)
def test_create_message(
    authorized_client,
    test_messages,
    test_user,
    title,
    content,
    receiver_id,
    status_code,
):
    create_data = {
        "title": title,
        "content": content,
        "receiver_id": receiver_id,
    }
    res = authorized_client.post("/messages", json=create_data)
    assert res.status_code == status_code

    if res.status_code != 422:
        new_message = message_schemas.Message(**res.json())

        print(new_message)

        assert new_message.title == create_data["title"]
        assert new_message.content == create_data["content"]
        assert new_message.receiver.id == create_data["receiver_id"]
        assert new_message.creator.id == test_user["id"]

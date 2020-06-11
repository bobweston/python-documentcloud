
def test_user(client):
    user = client.users.get(client.user_id)
    assert str(user) == user.username

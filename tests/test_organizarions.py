
def test_organization(client):
    user = client.users.get(client.user_id)
    organization = client.organizations.get(user.organization)
    assert str(organization) == organization.name

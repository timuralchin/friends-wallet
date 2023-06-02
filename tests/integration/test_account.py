from datetime import datetime

import pytest


@pytest.mark.django_db
class TestAccount:

    def test_get(self, authable_client, user):
        client = authable_client(user)
        response = client.get('/api/v1/account/')
        data = response.json()
        assert response.status_code == 200
        assert data['email'] == user.email
        assert data['first_name'] == user.first_name
        assert data['last_name'] == user.last_name
        assert data['username'] == user.username

    def test_patch(self, authable_client, user):
        client = authable_client(user)
        example_data = str(datetime.now().timestamp())
        response = client.patch(
            '/api/v1/account/',
            {
                'email': f'{example_data}@test.com',
            },
        )
        data = response.json()
        assert response.status_code == 200
        assert data['email'] == f'{example_data}@test.com'
        assert data['first_name'] == user.first_name
        assert data['last_name'] == user.last_name
        assert data['username'] == user.username

    def test_delete(self, authable_client, user):
        test_user = user
        client = authable_client(test_user)
        response = client.delete('/api/v1/account/')
        assert response.status_code == 204

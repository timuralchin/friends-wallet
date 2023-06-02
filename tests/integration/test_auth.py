from datetime import datetime

import pytest
from django.test import Client


@pytest.mark.django_db
class TestSignUp:

    def test_signup(self, client: Client):
        example_data = str(datetime.now().timestamp())
        response = client.post(
            '/api/v1/auth/signup/',
            {
                'email': f'{example_data}@test.com',
                'first_name': 'test',
                'last_name': 'test',
                'username': example_data,
                'password': 'qwerty!@#$%^',
            },
        )
        data = response.json()
        assert response.status_code == 201
        assert data['tokens']
        assert data['user']['email'] == f'{example_data}@test.com'
        assert data['user']['first_name'] == 'test'
        assert data['user']['last_name'] == 'test'
        assert data['user']['username'] == example_data

    def test_signup_with_invalid_password(self, client: Client):
        example_data = str(datetime.now().timestamp())
        response = client.post(
            '/api/v1/auth/signup/',
            {
                'email': f'{example_data}@test.com',
                'first_name': 'test',
                'last_name': 'test',
                'username': example_data,
                'password': '1234',
            },
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestLogout:

    def test_logout(self, auth_client):
        client, token = auth_client
        response = client.post(
            '/api/v1/auth/logout/',
            {
                'refresh': str(token),
            },
        )
        assert response.status_code == 205

from unittest.mock import MagicMock

import pytest

from src.database.models import User, Comment, Image
from src.services.auth import auth_service


@pytest.fixture()
def token(client, user, session, monkeypatch):
   """
    The token function is used to create a user..
    It returns an access token for use in other tests.
   """
   #  -----------------------------------------------1---------------------------------------------------

@pytest.fixture(scope="module")
def fix_comment():

    comment = {
        "text": "Test text for new comment",
        "id": 1,
        "created_at": "2023-06-20T12:00:00.062Z",
        "updated_at": None,
        "user_id": 1,
        "image_id": 1,
        "update_status": False
    }
    return comment


def test_create_comment(client, token):

    response = client.post(
        "api/comments/new/1", json={"text": "Test text for new comment"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200, response.text

    body_data = response.json()
    assert body_data == {
        "text": "Test text for new comment",
        "id": 1,
        "created_at": f"{body_data['created_at']}",
        "updated_at": None,
        "user_id": 1,
        "image_id": 1,
        "update_status": False
    }


def test_create_comment_2(client, token):

    response = client.post(
        "api/comments/new/1", json={"text": "Test text for new comment"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text


def test_single_comment(client, session, token):

    response = client.get("api/comments/single/1",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text


def test_by_user_comments(client, session, token):

    response = client.get(
        "api/comments/by_author/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text


def test_by_user_image_comments(client, session, token):

    response = client.get(
        "api/comments/image_by_author/1/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text


def test_edit_comment(client, session, token, user):

    response = client.put(
        "api/comments/edit/1", json={"text": "NEW Test text for new comment"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text


def test_delete_comment(client, session, token):

    response = client.put(
        "api/comments/edit/1", json={"text": "NEW Test text for new comment"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text

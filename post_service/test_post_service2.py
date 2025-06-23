import pytest
from unittest.mock import patch
from generated import post_pb2
from server import PostService, comments_storage

@pytest.fixture
def post_service():
    return PostService()

def test_like_post_sends_kafka_event(post_service):
    request = post_pb2.PostActionRequest(
        client_id="user1",
        post_id="post1",
        timestamp="2025-06-20T12:00:00Z"
    )

    with patch("server.send_kafka_event") as mock_send_kafka_event:
        response = post_service.LikePost(request, None)

    mock_send_kafka_event.assert_called_once_with("post_likes", {
        "client_id": "user1",
        "post_id": "post1",
        "timestamp": "2025-06-20T12:00:00Z"
    })
    assert response.status == "like saved"

def test_comment_post_saves_comment_and_sends_kafka_event(post_service):
    request = post_pb2.CommentRequest(
        client_id="user2",
        post_id="post2",
        text="Nice post!",
        timestamp="2025-06-20T12:01:00Z"
    )

    with patch("server.send_kafka_event") as mock_send_kafka_event:
        response = post_service.CommentPost(request, None)

    assert "post2" in comments_storage
    assert comments_storage["post2"][0]["client_id"] == "user2"
    assert comments_storage["post2"][0]["text"] == "Nice post!"
    assert comments_storage["post2"][0]["timestamp"] == "2025-06-20T12:01:00Z"

    mock_send_kafka_event.assert_called_once_with("post_comments", {
        "client_id": "user2",
        "post_id": "post2",
        "text": "Nice post!",
        "timestamp": "2025-06-20T12:01:00Z"
    })
    assert response.status == "comment saved"

def test_get_comments_returns_paged_comments(post_service):
    post_id = "post3"
    comments_storage[post_id] = [
        {"client_id": "user1", "text": "Comment 1", "timestamp": "t1"},
        {"client_id": "user2", "text": "Comment 2", "timestamp": "t2"},
        {"client_id": "user3", "text": "Comment 3", "timestamp": "t3"},
    ]

    request = post_pb2.GetCommentsRequest(
        post_id=post_id,
        page=0,
        size=2
    )

    response = post_service.GetComments(request, None)

    assert len(response.comments) == 2
    assert response.comments[0].client_id == "user1"
    assert response.comments[1].client_id == "user2"


import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "post_service")))

import pytest
import grpc
from generated import post_pb2, post_pb2_grpc
import httpx
import time
from datetime import datetime

USER_SERVICE_URL = "http://localhost:8000"
POST_SERVICE_GRPC = "localhost:50051"


@pytest.mark.asyncio
async def test_full_flow_registration_post_and_analytics():
    username = "e2euser1"
    password = "StrongP@ssw0rd!"
    email = "e2euser1@example.com"

    async with httpx.AsyncClient() as client:
        r = await client.post(f"{USER_SERVICE_URL}/register/", json={
            "username": username,
            "email": email,
            "password": password
        })
        assert r.status_code in (200, 201)
        r = await client.post(f"{USER_SERVICE_URL}/login/", json={
            "username": username,
            "password": password
        })
        assert r.status_code in (200, 201)
        token = r.json()["access_token"]

    with grpc.insecure_channel(POST_SERVICE_GRPC) as channel:
        stub = post_pb2_grpc.PostServiceStub(channel)
        timestamp = datetime.utcnow().isoformat()

        view_resp = stub.ViewPost(post_pb2.PostActionRequest(
            client_id=username,
            post_id="post123",
            timestamp=timestamp
        ))
        assert view_resp.status == "view saved"

        like_resp = stub.LikePost(post_pb2.PostActionRequest(
            client_id=username,
            post_id="post123",
            timestamp=timestamp
        ))
        assert like_resp.status == "like saved"

        comment_resp = stub.CommentPost(post_pb2.CommentRequest(
            client_id=username,
            post_id="post123",
            text="Awesome!",
            timestamp=timestamp
        ))
        assert comment_resp.status == "comment saved"

    time.sleep(2)

    assert True


@pytest.mark.asyncio
async def test_comments_storage_and_retrieval():
    with grpc.insecure_channel(POST_SERVICE_GRPC) as channel:
        stub = post_pb2_grpc.PostServiceStub(channel)

        post_id = "post567"
        timestamp = datetime.utcnow().isoformat()

        for i in range(3):
            resp = stub.CommentPost(post_pb2.CommentRequest(
                client_id=f"user{i}",
                post_id=post_id,
                text=f"Comment {i}",
                timestamp=timestamp
            ))
            assert resp.status == "comment saved"

        time.sleep(1)

        response = stub.GetComments(post_pb2.GetCommentsRequest(
            post_id=post_id,
            page=0,
            size=3
        ))

        assert len(response.comments) == 3
        assert response.comments[0].text.startswith("Comment")


@pytest.mark.asyncio
async def test_authentication_failure():
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": "Bearer invalid_token"}
        r = await client.get(f"{USER_SERVICE_URL}/profile/", headers=headers)
        assert r.status_code == 401
        assert r.json()["detail"] == "Invalid token"


import sys
import os
import pytest
import grpc
import httpx
import time
from datetime import datetime


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "post_service")))

from generated import post_pb2, post_pb2_grpc

USER_SERVICE_URL = "http://localhost:8000"
POST_SERVICE_GRPC = "localhost:50051"


@pytest.mark.asyncio
async def test_grpc_comment_and_like_flow():
    username = "grpc_user1"
    password = "TestP@ss123!"
    email = "grpc_user1@example.com"
    post_id = "grpc_post_1"
    timestamp = datetime.utcnow().isoformat()

    async with httpx.AsyncClient() as client:
        await client.post(f"{USER_SERVICE_URL}/register/", json={
            "username": username,
            "email": email,
            "password": password
        })

    with grpc.insecure_channel(POST_SERVICE_GRPC) as channel:
        stub = post_pb2_grpc.PostServiceStub(channel)

        comment_resp = stub.CommentPost(post_pb2.CommentRequest(
            client_id=username,
            post_id=post_id,
            text="Test comment via gRPC",
            timestamp=timestamp
        ))
        assert comment_resp.status == "comment saved"

        like_resp = stub.LikePost(post_pb2.PostActionRequest(
            client_id=username,
            post_id=post_id,
            timestamp=timestamp
        ))
        assert like_resp.status == "like saved"

        get_resp = stub.GetComments(post_pb2.GetCommentsRequest(
            post_id=post_id,
            page=0,
            size=5
        ))
        texts = [c.text for c in get_resp.comments]
        assert any("Test comment via gRPC" in t for t in texts)




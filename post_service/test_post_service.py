import grpc
import pytest
from datetime import datetime
from grpc import insecure_channel
from grpc import RpcError
from grpc._channel import _InactiveRpcError

from grpc import StatusCode
from grpc._cython.cygrpc import StatusCode as CyStatusCode

from grpc import StatusCode
from generated import post_pb2, post_pb2_grpc

@pytest.fixture(scope="module")
def grpc_stub():
    # Адрес и порт зависят от твоей конфигурации
    channel = insecure_channel("localhost:50051")
    stub = post_pb2_grpc.PostServiceStub(channel)
    return stub

def test_like_post(grpc_stub):
    response = grpc_stub.LikePost(post_pb2.PostActionRequest(
        client_id="user_001",
        post_id="post_001",
        timestamp=datetime.utcnow().isoformat()
    ))
    assert response.status == "like saved"

def test_view_post(grpc_stub):
    response = grpc_stub.ViewPost(post_pb2.PostActionRequest(
        client_id="user_002",
        post_id="post_002",
        timestamp=datetime.utcnow().isoformat()
    ))
    assert response.status == "view saved"

def test_comment_post(grpc_stub):
    response = grpc_stub.CommentPost(post_pb2.CommentRequest(
        client_id="user_003",
        post_id="post_003",
        text="Интересный пост!",
        timestamp=datetime.utcnow().isoformat()
    ))
    assert response.status == "comment saved"


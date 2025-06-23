import sys
import os
import pytest
import grpc
import httpx
import time
from datetime import datetime

# Добавляем post_service в PYTHONPATH для корректного импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "post_service")))

from generated import post_pb2, post_pb2_grpc


USER_SERVICE_URL = "http://localhost:8000"
API_GATEWAY_URL = "http://localhost:8080"
POST_SERVICE_GRPC = "localhost:50051"


@pytest.mark.asyncio
async def test_post_stats_end_to_end():
    """
    Сквозной тест:
    - Регистрация пользователя
    - Действия над постом (view, like, comment)
    - Получение статистики через API Gateway
    """
    username = "e2e_user_stats"
    password = "StrongP@ssw0rd!"
    email = "e2e_user_stats@example.com"
    post_id = "post_xyz"

    async with httpx.AsyncClient() as client:
        # Регистрация
        await client.post(f"{USER_SERVICE_URL}/register/", json={
            "username": username,
            "email": email,
            "password": password
        })

        # Логин
        r = await client.post(f"{USER_SERVICE_URL}/login/", json={
            "username": username,
            "password": password
        })
        token = r.json()["access_token"]

    # Выполнение действий над постом через gRPC
    with grpc.insecure_channel(POST_SERVICE_GRPC) as channel:
        stub = post_pb2_grpc.PostServiceStub(channel)
        timestamp = datetime.utcnow().isoformat()

        stub.ViewPost(post_pb2.PostActionRequest(
            client_id=username,
            post_id=post_id,
            timestamp=timestamp
        ))
        stub.LikePost(post_pb2.PostActionRequest(
            client_id=username,
            post_id=post_id,
            timestamp=timestamp
        ))
        stub.CommentPost(post_pb2.CommentRequest(
            client_id=username,
            post_id=post_id,
            text="Interesting post!",
            timestamp=timestamp
        ))

    # Подождать, пока аналитика обработает данные
    time.sleep(2)

    # Получить статистику через API Gateway
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_GATEWAY_URL}/post/{post_id}/stats")
        assert r.status_code == 200
        stats = r.json()
        assert stats["post_id"] == post_id
        assert stats["views"] >= 1
        assert stats["likes"] >= 1
        assert stats["comments"] >= 1


@pytest.mark.asyncio
async def test_top_posts_by_likes():
    """
    Сквозной тест:
    - Несколько пользователей лайкают пост
    - Проверка, что пост попал в топ по лайкам через API Gateway
    """
    post_id = "post_top_123"
    timestamp = datetime.utcnow().isoformat()

    with grpc.insecure_channel(POST_SERVICE_GRPC) as channel:
        stub = post_pb2_grpc.PostServiceStub(channel)

        for i in range(5):
            client_id = f"user_{i}"
            stub.LikePost(post_pb2.PostActionRequest(
                client_id=client_id,
                post_id=post_id,
                timestamp=timestamp
            ))

    time.sleep(2)

    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_GATEWAY_URL}/posts/top?stat_type=likes")
        assert r.status_code == 200
        top_posts = r.json()["posts"]
        post_ids = [p["post_id"] for p in top_posts]
        assert post_id in post_ids


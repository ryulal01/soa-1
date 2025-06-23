import pytest
from unittest.mock import patch, MagicMock
import analytics_pb2
from server import AnalyticsService

@pytest.fixture
def analytics_service():
    with patch("server.Storage") as MockStorage:
        mock_storage = MagicMock()
        MockStorage.return_value = mock_storage
        service = AnalyticsService()
        service.storage = mock_storage
        return service

def test_get_post_stats_returns_correct_data(analytics_service):
    analytics_service.storage.get_post_stats.return_value = (10, 5, 3)

    request = analytics_pb2.PostIdRequest(post_id="post1")
    response = analytics_service.GetPostStats(request, None)

    analytics_service.storage.get_post_stats.assert_called_once_with("post1")
    assert response.post_id == "post1"
    assert response.views == 10
    assert response.likes == 5
    assert response.comments == 3

def test_get_post_views_dynamics_returns_items(analytics_service):
    analytics_service.storage.get_dynamics.return_value = [
        ("2025-06-20", 7), 
        ("2025-06-21", 4)
    ]

    request = analytics_pb2.PostIdRequest(post_id="post2")
    response = analytics_service.GetPostViewsDynamics(request, None)

    analytics_service.storage.get_dynamics.assert_called_once_with("post2", "view")
    assert len(response.items) == 2
    assert response.items[0].date == "2025-06-20"
    assert response.items[0].count == 7
    assert response.items[1].date == "2025-06-21"
    assert response.items[1].count == 4

def test_get_top_posts_returns_list(analytics_service):
    analytics_service.storage.get_top_posts.return_value = [
        ("post1", 15), 
        ("post2", 10)
    ]

    request = analytics_pb2.TopRequest(stat_type=1)  # LIKES
    response = analytics_service.GetTopPosts(request, None)

    analytics_service.storage.get_top_posts.assert_called_once_with("like")
    assert len(response.posts) == 2
    assert response.posts[0].post_id == "post1"
    assert response.posts[0].count == 15
    assert response.posts[1].post_id == "post2"
    assert response.posts[1].count == 10


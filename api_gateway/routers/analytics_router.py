from fastapi import APIRouter
from grpc_client import AnalyticsGRPCClient
from analytics_pb2 import TopRequest

router = APIRouter()
grpc_client = AnalyticsGRPCClient()

@router.get("/post/{post_id}/stats")
def get_post_stats(post_id: str):
    response = grpc_client.get_post_stats(post_id)
    return {
        "post_id": response.post_id,
        "views": response.views,
        "likes": response.likes,
        "comments": response.comments
    }

@router.get("/posts/top")
def get_top_posts(stat_type: str):
    stat_map = {
        "views": TopRequest.StatType.VIEWS,
        "likes": TopRequest.StatType.LIKES,
        "comments": TopRequest.StatType.COMMENTS
    }
    stat_enum = stat_map[stat_type]

    response = grpc_client.get_top_posts(stat_enum)
    return {
        "posts": [
            {"post_id": post.post_id, "count": post.count}
            for post in response.posts
        ]
    }


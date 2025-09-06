import grpc
from concurrent import futures
import analytics_pb2
import analytics_pb2_grpc
from storage import Storage

class AnalyticsService(analytics_pb2_grpc.AnalyticsServiceServicer):
    def __init__(self):
        self.storage = Storage()

    def GetPostStats(self, request, context):
        views, likes, comments = self.storage.get_post_stats(request.post_id)
        return analytics_pb2.PostStatsResponse(
            post_id=request.post_id,
            views=views,
            likes=likes,
            comments=comments
        )

    def GetPostViewsDynamics(self, request, context):
        rows = self.storage.get_dynamics(request.post_id, 'view')
        return analytics_pb2.DynamicsResponse(
            items=[
                analytics_pb2.DynamicsItem(date=str(date), count=count)
                for date, count in rows
            ]
        )

    def GetPostLikesDynamics(self, request, context):
        rows = self.storage.get_dynamics(request.post_id, 'like')
        return analytics_pb2.DynamicsResponse(
            items=[
                analytics_pb2.DynamicsItem(date=str(date), count=count)
                for date, count in rows
            ]
        )

    def GetPostCommentsDynamics(self, request, context):
        rows = self.storage.get_dynamics(request.post_id, 'comment')
        return analytics_pb2.DynamicsResponse(
            items=[
                analytics_pb2.DynamicsItem(date=str(date), count=count)
                for date, count in rows
            ]
        )

    def GetTopPosts(self, request, context):
        type_map = {0: 'view', 1: 'like', 2: 'comment'}
        rows = self.storage.get_top_posts(type_map[request.stat_type])
        return analytics_pb2.TopPostsResponse(
            posts=[
                analytics_pb2.TopPostsResponse.PostInfo(post_id=post_id, count=count)
                for post_id, count in rows
            ]
        )

    def GetTopUsers(self, request, context):
        type_map = {0: 'view', 1: 'like', 2: 'comment'}
        rows = self.storage.get_top_users(type_map[request.stat_type])
        return analytics_pb2.TopUsersResponse(
            users=[
                analytics_pb2.TopUsersResponse.UserInfo(user_id=user_id, count=count)
                for user_id, count in rows
            ]
        )


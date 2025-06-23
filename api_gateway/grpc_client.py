import grpc
import analytics_pb2
import analytics_pb2_grpc

class AnalyticsGRPCClient:
    def __init__(self, host='analytics_service', port=50051):  # важно! host — docker имя твоего analytics_service
        channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = analytics_pb2_grpc.AnalyticsServiceStub(channel)

    def get_post_stats(self, post_id: str):
        request = analytics_pb2.PostIdRequest(post_id=post_id)
        return self.stub.GetPostStats(request)

    def get_top_posts(self, stat_type: int):
        request = analytics_pb2.TopRequest(stat_type=stat_type)
        return self.stub.GetTopPosts(request)



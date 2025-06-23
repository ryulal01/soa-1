import grpc
import analytics_pb2
import analytics_pb2_grpc

class AnalyticsGRPCClient:
    def __init__(self, host='localhost', port=50051):
        channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = analytics_pb2_grpc.AnalyticsServiceStub(channel)

    def get_post_stats(self, post_id):
        request = analytics_pb2.PostIdRequest(post_id=post_id)
        return self.stub.GetPostStats(request)


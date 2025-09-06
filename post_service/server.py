import grpc
from concurrent import futures
from generated import post_pb2, post_pb2_grpc
from kafka_producer import send_kafka_event
import time

comments_storage = {}

class PostService(post_pb2_grpc.PostServiceServicer):
    def LikePost(self, request, context):
        send_kafka_event("post_likes", {
            "client_id": request.client_id,
            "post_id": request.post_id,
            "timestamp": request.timestamp,
        })
        return post_pb2.PostActionResponse(status="like saved")

    def ViewPost(self, request, context):
        send_kafka_event("post_views", {
            "client_id": request.client_id,
            "post_id": request.post_id,
            "timestamp": request.timestamp,
        })
        return post_pb2.PostActionResponse(status="view saved")

    def CommentPost(self, request, context):
        if request.post_id not in comments_storage:
            comments_storage[request.post_id] = []
        comments_storage[request.post_id].append({
            "client_id": request.client_id,
            "text": request.text,
            "timestamp": request.timestamp
        })

        send_kafka_event("post_comments", {
            "client_id": request.client_id,
            "post_id": request.post_id,
            "text": request.text,
            "timestamp": request.timestamp,
        })
        return post_pb2.PostActionResponse(status="comment saved")

    def GetComments(self, request, context):
        post_comments = comments_storage.get(request.post_id, [])
        start = request.page * request.size
        end = start + request.size
        selected = post_comments[start:end]

        return post_pb2.GetCommentsResponse(
            comments=[
                post_pb2.CommentResponse(
                    client_id=c["client_id"],
                    text=c["text"],
                    timestamp=c["timestamp"]
                ) for c in selected
            ]
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    post_pb2_grpc.add_PostServiceServicer_to_server(PostService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("PostService gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()


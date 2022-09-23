import grpc

from proto import HrlloWorldService_pb2
from proto import HrlloWorldService_pb2_grpc

if __name__ == "__main__":
    client = HrlloWorldService_pb2_grpc.HelloWorldStub(grpc.insecure_channel("0.0.0.0:50051"))
    response = client.SendSms(
        HrlloWorldService_pb2.HelloWorldRequest(name="Word"))
    print(response.message)

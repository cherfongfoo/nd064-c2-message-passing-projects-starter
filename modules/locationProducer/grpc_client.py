import locationEvent_pb2
import locationEvent_pb2_grpc
import grpc

print("send location")

channel = grpc.insecure_channel("localhost:30051")
stub = locationEvent_pb2_grpc.EventCoordinatesServiceStub(channel)

# Update this with desired payload
user_location = locationEvent_pb2.EventCoordinatesMessage(
    personId=1,
    latitude=-900,
    longitude=30
)

user_location_2 = locationEvent_pb2.EventCoordinatesMessage(
    personId=8,
    latitude=-500,
    longitude=10
)

response_1 = stub.Create(user_location)
response_2 = stub.Create(user_location_2)

print("Done")
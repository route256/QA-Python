import grpc

from framework.grpc.clients.ozonmp.act_device_api.v1.act_device_api_pb2_grpc import (
    ActDeviceApiServiceStub)
from framework.grpc.clients.ozonmp.act_device_api.v1.act_device_api_pb2 import (
    DescribeDeviceV1Request, CreateDeviceV1Request
)


class DeviceAPIGRPC:
    def __init__(self, host):
        self._channel = grpc.insecure_channel(host)
        self._stub = ActDeviceApiServiceStub(self._channel)

    def get_device(self, device_id):
        request = DescribeDeviceV1Request(device_id=device_id)
        response = self._stub.DescribeDeviceV1(request)
        return response

    def create_device(self, platform, user_id):
        request = CreateDeviceV1Request(platform=platform, user_id=user_id)
        response = self._stub.CreateDeviceV1(request)
        return response

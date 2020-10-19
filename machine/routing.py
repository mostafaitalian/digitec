from django.urls import path, re_path
from .consumers import MachineConsumer,MachineConsumer1, MachineConsumer2,MachineConsumer3

websocket_urlpatterns = [
    path('machine/list1/', MachineConsumer3),
    path('customer/list/', MachineConsumer3),
    path('machine/detail/<pk>/', MachineConsumer)   
]
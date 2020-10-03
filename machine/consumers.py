# from channels.consumers import WebSoketConsumer
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from engineer.models import Engineer
from channels.db import database_sync_to_async
from asgiref.sync import AsyncToSync
import json

class MachineConsumer(WebsocketConsumer):
    def connect(self):
        # if self.scope['user'].is_authenticated:

        #     self.scope['url_route'].kwargs['machine_id']
        #     self.accept()
        # else:
        #     self.close()
        
        
        self.accept()
        machine_pk = self.scope['url_route']['kwargs']['pk']
        self.send(text_data='your pk is %s' % machine_pk)


        
    def receive(self, event):
        self.send(text_data='you data is reaching us')

    def disconnect(self):
        # self.close()
        pass


class MachineConsumer1(WebsocketConsumer):


    def connect(self):
        self.accept()
        user = self.scope['user']
        # user_json = json.dumps(user)
        # user_json2 = json.loads({'user':user})
        # engineer_name = database_sync_to_async(Engineer.objects.get)(user=user).name
        # print(engineer.name)

        self.send(text_data=user.username)

        # self.send(text_data=user_json)
        # self.send(text_data=user_json2)
    def receive(self, text_data=None, bytes_data=None):
        # print(text_data)
        self.send(text_data='your data is got '+ text_data)

        # return super().receive(text_data=text_data, bytes_data=bytes_data)

counter=0
class MachineConsumer2(JsonWebsocketConsumer):
    # counter=0

    def connect(self):
        self.accept()
        # self.send_json(content={"message":"hello"})
        
    def recieve_json(self,c):
        self.send_json(c)
    
    def disconnect(self):
        pass


class MachineConsumer3(WebsocketConsumer):
    counter=0
    def connect(self):
        super().connect()

        # engineer=Engineer.objects.get(user__id=self.scope['user'].id)

        # self.accept()
        self.send(text_data=self.scope['user'])


    def receive(self, text_data=None, bytes_data=None):
        # print(text_data)
        # engineer=Engineer.objects.get(user__id=self.scope['user'].id)
        # counter +=1 
        # self.send(text_data='your data is got ')
        # self.send('hhhhhhhhh')
        self.send(text_data='hhhh')
        self.send(text_data='kkkkkk')
        self.send(text_data=text_data)

        return super().recieve(text_data=None)

    
    def disconnect(self):
        self.close()

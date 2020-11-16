# from channels.consumers import WebSoketConsumer
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from engineer.models import Engineer
from .models import Call
from channels.db import database_sync_to_async
from asgiref.sync import AsyncToSync
import json

import datetime

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
        # self.send(text_data=self.scope['user'].username)


    def receive(self, text_data=None, bytes_data=None):
        # print(text_data)
        # engineer=Engineer.objects.get(user__id=self.scope['user'].id)
        # counter +=1 
        # self.send(text_data='your data is got ')
        # self.send('hhhhhhhhh')
        print(text_data)
        if self.scope['user'].is_superuser:
            total_calls = Call.objects.all().count()
            unassigned_engineer_calls = Call.objects.filter(status='unassigned').count()
            pending_engineer_calls = Call.objects.filter(status='incomplete').count()
            dispatched_engineer_calls = Call.objects.filter(status='dispatched').count()
            completed_engineer_calls = Call.objects.filter(status='completed').count()
            self.send(text_data='You have {} calls.\nYou have {} calls unassigned.\nYou have {} calls dispatched.\nYou have {} calls pending.\nYou have {} calls completed.'.format(total_calls, unassigned_engineer_calls, dispatched_engineer_calls, pending_engineer_calls, completed_engineer_calls))
            self.send(text_data='s' + str(unassigned_engineer_calls))
            self.send(text_data='d' + str(dispatched_engineer_calls))
            self.send(text_data='i' + str(pending_engineer_calls))
            self.send(text_data='c' + str(completed_engineer_calls))
        elif self.scope['user'].engineer and self.scope['user'].is_authenticated:
            dispatched_engineer_calls = Call.objects.filter(engineer__user=self.scope['user']).filter(status='dispatched').count()
            completed_engineer_calls = Call.objects.filter(engineer__user=self.scope['user']).filter(status='completed').count()
            pending_engineer_calls = Call.objects.filter(engineer__user=self.scope['user']).filter(status='incomplete').count()
            
            dispatched_engineer_calls_before_second = Call.objects.filter(engineer__user=self.scope['user']).filter(status='dispatched').filter(assigned_date__lt=datetime.datetime.now()-datetime.timedelta(seconds=1)).count()
            self.send(text_data='You have {} calls dispatched.\nYou have {} calls still at pending stage.\nYou have {} calls still at completed stage.'.format(dispatched_engineer_calls, pending_engineer_calls, completed_engineer_calls))
            self.send(text_data='d' + str(dispatched_engineer_calls))
            self.send(text_data='i' + str(pending_engineer_calls))
            self.send(text_data='c' + str(completed_engineer_calls))            
        # if(dispatched_engineer_calls != dispatched_engineer_calls_before_second):
        #     # i=500
        #     # while(i<501):
        #     #     i=i-1
            
        #     self.send(text_data='you got a new call')
        # self.send(text_data='kkkkkk')
        # self.send(text_data='{}'.format(dispatched_engineer_calls))

        return super().recieve(text_data=text_data)



    
    def disconnect(self):
        self.close()
    def call_update(self, event):
        self.send({
            'type': 'websocket.send',
            'text':event['content'],
        })
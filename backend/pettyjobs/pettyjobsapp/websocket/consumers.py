from channels.generic.websocket import AsyncWebsocketConsumer
import json
from ..models import Job
from ..serializers import JobSerializer
from asgiref.sync import sync_to_async

class testConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.accept()

class JobConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connected to WebSocket")
        self.user = self.scope["user"]
        print(f"User connected: {self.user}")

        if not self.user.is_authenticated:
            print(f"User {self.user} is not authenticated, closing connection.")
            await self.close()
            return

        if self.user.user_type != 'in_charge':
            print(f"User {self.user} is not an 'in_charge' user, closing connection.")
            await self.close()
            return

        self.user_type = self.user.user_type
        self.sub_type = self.user.sub_type
        print(f"User type: {self.user_type}, Sub type: {self.sub_type}")

        self.group_name = f'jobs_{self.user.sub_type}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        print(f"User {self.user} added to group {self.group_name}")

        await self.accept()
        print("WebSocket connection accepted")

        await self.send_filtered_jobs()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def job_created(self, event):
        await self.send(text_data=json.dumps({
            'action': 'job_created',
            'job': event['job']
        }))

    async def job_updated(self, event):
        await self.send(text_data=json.dumps({
            'action': 'job_updated',
            'job': event['job']
        }))

    async def job_deleted(self, event):
        await self.send(text_data=json.dumps({
            'action': 'job_deleted',
            'job_id': event['job']['id'],
            'job_type': event['job']['job_type'],
        }))

    async def send_filtered_jobs(self):
        if self.user_type == 'in_charge' and self.sub_type:
            jobs = await sync_to_async(list)(Job.objects.filter(job_type=self.sub_type))
        else:
            return
            
        serializer = JobSerializer(jobs, many=True)

        await self.send(text_data=json.dumps({
            'jobs': serializer.data
        }))

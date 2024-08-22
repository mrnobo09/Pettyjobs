from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsWorker

class WorkerView(APIView):
    permission_classes = [IsAuthenticated, IsWorker]

    def get(self, request):
        return Response({"message": "Hello, Worker!"})

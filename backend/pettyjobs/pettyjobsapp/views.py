from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsWorker,IsInCharge

from .serializers import JobSerializer
from .models import User, Job

class WorkerJobList(APIView):
    permission_classes = [IsAuthenticated, IsInCharge]

    def get(self, request):
        incharge = get_object_or_404(User,id = request.user.id)

        jobs = Job.objects.filter(job_type = incharge.sub_type, status = 'in_progress')

        serializer = JobSerializer(jobs,many=True)

        return Response(serializer.data)

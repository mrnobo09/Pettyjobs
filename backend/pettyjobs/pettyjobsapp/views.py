from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsWorker,IsInCharge
from django.db.models import Q

from .serializers import JobSerializer
from .models import User, Job, JobImages

class WorkerJobList(APIView):
    permission_classes = [IsAuthenticated, IsInCharge]

    def get(self, request):
        incharge = get_object_or_404(User,id = request.user.id)

        jobs = Job.objects.filter(job_type = incharge.sub_type, status = 'in_progress')

        serializer = JobSerializer(jobs,many=True)

        return Response(serializer.data)
    
class History(APIView):
    permission_classes = [IsAuthenticated, IsWorker]

    def get(self, request):
        worker = get_object_or_404(User, id=request.user.id)
        
        jobs = Job.objects.filter(
            job_type=worker.sub_type,
            uploaded_by=worker
        )

        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    
class postJob(APIView):
    permission_classes = [IsAuthenticated,IsWorker]

    def post(self,request):
        data = request.data
        worker = get_object_or_404(User,id=request.user.id)

        title = data.get('title')
        location = data.get('location')
        description = data.get('description')
        job_type = data.get('jobType')
        criticality = data.get('criticality')
        uploaded_by = worker

        job = Job.objects.create(
            title = title,
            location = location,
            description = description,
            job_type = job_type,
            criticality = criticality,
            uploaded_by = uploaded_by
        )

        images = data.getlist('images')

        for image in images:
            JobImages.objects.create(job = job,image=image)

        return Response({"message":"Job Successfully Created","job_id":job.id}, status=status.HTTP_201_CREATED)








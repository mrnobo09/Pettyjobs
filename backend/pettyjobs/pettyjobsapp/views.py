from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsWorker,IsInCharge,IsContractor
from django.db.models import Q
from django.utils import timezone

from .serializers import JobSerializer,JobHistorySerializer
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
            uploaded_by=worker
        )

        serializer = JobHistorySerializer(jobs, many=True)
        return Response(serializer.data)
    
class viewJob_as_worker(APIView):
    permission_classes = [IsAuthenticated,IsWorker]

    def get(self,request):
        job_id = request.query_params.get('jobID')
        job =  get_object_or_404(Job,id = job_id)

        serializer = JobSerializer(job)

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
    

class ApproveJob(APIView):

    permission_classes = [IsAuthenticated,IsInCharge]

    def post(self,request):
        job = get_object_or_404(Job,id=request.job_id)
        inCharge = get_object_or_404(User,id=request.user.id)
        contractor = get_object_or_404(User,id = request.contractor_id)

        job.status = Job.IN_PROGRESS
        job.approved_by = inCharge
        job.accepted_by = contractor
        job.approved_at = timezone.now()

        job.save()

        return Response({"message":"Job Successfully Approved and assigned to {contractor.full_name}"}, status = status.HTTP_201_CREATED)


class accept_or_reject_reviewed_job_as_worker(APIView):
    permission_classes = [IsAuthenticated,IsWorker]

    def post(self,request):
        worker = get_object_or_404(User,id = request.user.id)
        job = get_object_or_404(Job,id = request.data['job_id'],uploaded_by = worker)
        approved = request.data['approved']

        try:
             if approved is not None:
                if approved:
                    job.status = Job.FINAL
                else: 
                    job.status = Job.IN_PROGRESS

                job.save()
                return Response({"message":"Job Successfully Approved","job_id":job.id}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            return Response({"message":"Job Approval Failed","job_id":job.id}, status=status.HTTP_400_BAD_REQUEST)
        

    
        

    


        













from django.urls import path
from . import views

urlpatterns = [
    path('job/',views.WorkerJobList.as_view()),
    path('history/',views.History.as_view()),
    path('postJob/',views.postJob.as_view()),
    path('approveJob/',views.ApproveJob.as_view()),
    path('view_job_as_contractor/',views.viewJob_as_worker.as_view()),
    path('accept_or_reject_reviewed_job_as_worker/',views.accept_or_reject_reviewed_job_as_worker.as_view())
]

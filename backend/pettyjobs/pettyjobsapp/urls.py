
from django.urls import path
from . import views

urlpatterns = [
    path('job/',views.WorkerJobList.as_view()),
    path('history/',views.History.as_view()),
    path('postJob/',views.postJob.as_view())
]

from django.urls import path, include
from task.apps import TaskConfig

app_name = TaskConfig.name

urlpatterns = [
    path('api/', include('task.api.urls'), name='task-api'),
]

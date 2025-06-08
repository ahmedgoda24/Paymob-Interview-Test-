from django.urls import path, include


urlpatterns = [
    path('v1/task/', include('task.api.v1.urls'), name='task-api-v1'),
]

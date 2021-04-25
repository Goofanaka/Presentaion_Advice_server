from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # face url 추가
    path('face/', include('face_test.urls')),
]

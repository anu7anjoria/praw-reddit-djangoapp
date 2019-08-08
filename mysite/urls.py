from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url('admin/', admin.site.urls),
    url('r/', include('reddit.urls')),
    #add Here some index page   127.0.0.1:8000/_____
]
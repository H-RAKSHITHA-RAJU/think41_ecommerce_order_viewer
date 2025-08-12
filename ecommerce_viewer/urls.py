from django.contrib import admin
from django.urls import path, include # <-- Is 'include' here?

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('viewer.urls')), # <-- Is there a comma after this line?
]
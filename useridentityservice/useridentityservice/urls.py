
# from django.contrib import admin
from django.urls import path
from contactmanagement.views import probe,ContactManagement

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',probe,name='Probe_Check'),
    path('identity/',ContactManagement.as_view(),name='identity'),

]

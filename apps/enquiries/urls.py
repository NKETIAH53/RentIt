from django.urls import path
from . import views


urlpatterns = [
    path('', views.send_enquiry_mail, name='send-enquiry')
]
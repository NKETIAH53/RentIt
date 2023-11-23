from django.urls import path
from . import views


urlpatterns = [
    path('<str:profile_id>/', views.agent_review, name='add-rating')
]
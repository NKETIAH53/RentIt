from django.urls import path
from .views import AgentListAPIView, get_all_top_agents, UserProfileAPIView, ProfileUpdateAPIView


urlpatterns = [
    path('me/', UserProfileAPIView.as_view(), name='get_profile'),
    path('<str:username>/update', ProfileUpdateAPIView.as_view(), name='update_profile'),
    path('agents/', AgentListAPIView.as_view(), name='all_agents'),
    path('top-agents/', get_all_top_agents, name='top_agents')
]
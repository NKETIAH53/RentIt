from django.urls import path
from . import views


urlpatterns = [
    path('', views.PropertiesListAPIView.as_view(), name='properties'),
    path('<str:slug>/', views.PropertyDetailAPIView.as_view(), name='property_details'),
    path('<str:slug>', views.update_property, name='update_property'),
    path('<str:slug>/images/', views.upload_property_image, name='upload_image'),
    path('agent/', views.AgentPropertyListAPIView.as_view(), name='agent_properties'),
    path('views/', views.PropertyViewsAPIView.as_view(), name='property_views'),
    path('search', views.PropertySearchAPIView.as_view(), name='search_property'),
]
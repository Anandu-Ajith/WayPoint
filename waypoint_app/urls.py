from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .import views

router = DefaultRouter()
router.register(r'destinations', DestinationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('detail/<int:pk>/',DestinationDetail.as_view(),name='detail'),
    path('update/<int:pk>/',DestinationUpdate.as_view(),name='update'),
    path('delete/<int:pk>/',DestinationDelete.as_view(),name='delete'),
    path('search/<str:Name>/',DestinationSearch.as_view(),name='search'),


    path('create_destination/',views.create_Destination,name='create_destination'),
    path('destination_fetch/<int:id>/',views.destination_fetch,name='destination_fetch'),
    path('destination_delete/<int:id>/', views.destination_delete, name='destination_delete'),
    path('update_destination/<int:id>/', views.update_destination, name='update_destination'),
    path('update_destination_form/<int:id>/', views.destination_update_form, name='update_destination_form'),
    path('index/', views.index, name='index'),
    path('update_detail<int:id>/', views.update_detail, name='update_detail'),

]
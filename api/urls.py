from django.urls import path
from .views import ParcelAPIView, DetailAPIView, BecomeTravelerView, PNRDelete, PNRList

urlpatterns = [
    path('parcels/<int:parcel_id>/become-traveler/', BecomeTravelerView.as_view()),
    path('<int:pk>/', DetailAPIView.as_view()),
    path('', ParcelAPIView.as_view()),
    path("pnr/", PNRList.as_view()),
    path("pnr/<str:pnr_number>/", PNRDelete.as_view()),
]
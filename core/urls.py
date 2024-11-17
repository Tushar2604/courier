from django.urls import path
from .views import user_page, home_page, CustomLoginView, logout_view, SignupPage, ParcelCreate, ParcelUpdate, ParcelDetail, ParcelDelete, TravelCreate, TravelUpdate, TravelDelete, BecomeTravelerView, ReviewRequestsView, ConfirmTravelerView, mark_notification_as_read, PnrValidationView

urlpatterns = [
    path('', home_page, name='home_page'), # url for the homepage
    path('user/', user_page, name='user_page'),
    path('login/', CustomLoginView.as_view(), name='login'), # class-based view for sign-in
    path('logout/', logout_view, name='logout'), # add the logout path
    path('signup/', SignupPage.as_view(), name='signup'), # clas-based view for signup
    path('parcel-create/', ParcelCreate.as_view(), name='parcel-create'), # class-based view for creating a new parcel
    path('parcel-update/<int:pk>/', ParcelUpdate.as_view(), name='parcel-update'), # class-based view for updating a parcel
    path('parcel/<int:pk>/', ParcelDetail.as_view(), name='parcel'), #class-based view for parcel detail
    path('parcel-delete/<int:pk>/', ParcelDelete.as_view(), name='parcel-delete'), # class-based view for deleting a parcel
    path('travel-create/', TravelCreate.as_view(), name='travel-create'),  # class-based view for creating a new travel
    path('travel-update/<int:pk>/', TravelUpdate.as_view(), name='travel-update'), # class-based view for updating travel details
    path('travel-delete/<int:pk>/', TravelDelete.as_view(), name='travel-delete'), # class-based view for deleting a travel detail
    path('become_traveler/<int:parcel_id>/', BecomeTravelerView.as_view(), name='become_traveler'), # class-based view for becoming traveler
    path('review_requests/', ReviewRequestsView.as_view(), name='review_requests'),
    path('confirm_traveler/<int:message_id>/', ConfirmTravelerView.as_view(), name='confirm_traveler'),
    path('mark_notification_as_read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
    #path('validate_pnr/', ValidatePNRAndRouteView.as_view(), name='validate_pnr'),
    path('pnr-validation/', PnrValidationView.as_view(), name='pnr_validation_page'),
]
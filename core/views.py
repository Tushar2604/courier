from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Parcel, TravelDetails, Message, Notification
from django.utils import timezone
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.views.generic import View, ListView
from django.views import View
import requests
import json
from .services import check_pnr_status, verify_route

# Create your views here.
def logout_view(request):
    # print ("abc")
    logout(request)
    return redirect('home_page')

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('user_page')
    
class SignupPage(FormView):
    template_name = 'core/signup.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('user_page')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignupPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('user_page')
        return super(SignupPage, self).get(*args, **kwargs)

@login_required
def user_page(request):
    #print(request.__dict__)
    parcels = Parcel.objects.filter(~Q(sender=request.user))
    #parcels = Parcel.objects.all()
    myparcels = Parcel.objects.filter(Q(sender=request.user))
    travel_details = TravelDetails.objects.filter(~Q(traveler=request.user))
    my_travel_details = TravelDetails.objects.filter(Q(traveler=request.user))
    notifications = Notification.objects.filter(user=request.user, read=False)
    return render(request, 'core/user_page.html', {
        'parcels': parcels,
        'myparcels': myparcels,
        'travel_details': travel_details,
        'my_travel_details': my_travel_details,
        'notifications': notifications,
    })

def home_page(request):
    #print(request.__dict__)
    if request.user.is_authenticated:
        return redirect('user_page')
    return render(request, 'core/home_page.html')

class ParcelCreate(LoginRequiredMixin, CreateView):
    model = Parcel
    fields = ['description', 'weight', 'origin', 'destination', 'deadline']
    template_name = 'core/parcel_edit.html'

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('user_page')
        return reverse_lazy('home_page')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(ParcelCreate, self).form_valid(form)

class ParcelUpdate(LoginRequiredMixin, UpdateView):
    model = Parcel
    fields = ['description', 'weight', 'origin', 'destination', 'deadline']
    template_name = 'core/parcel_edit.html'

    def dispatch(self, request, *args, **kwargs):
        parcel = self.get_object()
        if parcel.sender != self.request.user:
            raise PermissionDenied("You are not allowed to edit this parcel.")
        return super(ParcelUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('user_page')
        return reverse_lazy('home_page')
    def form_valid(self, form):
        return super(ParcelUpdate, self).form_valid(form)

class ParcelDetail(LoginRequiredMixin, DetailView):
    model = Parcel
    context_object_name = 'parcel'
    
class ParcelDelete(LoginRequiredMixin, DeleteView):
    model = Parcel
    context_object_name = 'parcel'

    def dispatch(self, request, *args, **kwargs):
        parcel = self.get_object()
        if parcel.sender != self.request.user:
            raise PermissionDenied("You are not allowed to delete this parcel.")
        return super(ParcelDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('user_page')
        return reverse_lazy('home_page')

class TravelCreate(LoginRequiredMixin, CreateView):
    model = TravelDetails
    fields = ['origin', 'destination', 'travel_date']
    template_name = 'core/travel_create.html'

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('user_page')
        return reverse_lazy('home_page')

    def form_valid(self, form):
        form.instance.traveler = self.request.user
        return super(TravelCreate, self).form_valid(form)

class TravelUpdate(LoginRequiredMixin, UpdateView):
    model = TravelDetails
    fields = ['origin', 'destination', 'travel_date']
    template_name = 'core/travel_create.html'

    def dispatch(self, request, *args, **kwargs):
        parcel = self.get_object()
        if parcel.traveler != self.request.user:
            raise PermissionDenied("You are not allowed to edit this travel details.")
        return super(TravelUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('user_page')
        return reverse_lazy('home_page')
    def form_valid(self, form):
        return super(TravelUpdate, self).form_valid(form)

class TravelDelete(LoginRequiredMixin, DeleteView):
    model = TravelDetails
    context_object_name = 'travel'

    def dispatch(self, request, *args, **kwargs):
        parcel = self.get_object()
        if parcel.traveler != self.request.user:
            raise PermissionDenied("You are not allowed to delete this travel detail.")
        return super(TravelDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('user_page')
        return reverse_lazy('home_page')

class BecomeTravelerView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        parcel_id = self.kwargs.get('parcel_id')
        parcel = get_object_or_404(Parcel, id=parcel_id)

        sender_origin = parcel.origin
        sender_destination = parcel.destination

        return redirect(f"{reverse('pnr_validation_page')}?sender_origin={sender_origin}&sender_destination={sender_destination}")
    
class PnrValidationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        sender_origin = request.GET.get('sender_origin')
        sender_destination = request.GET.get('sender_destination')
        return render(request, 'core/pnr_valid.html', {
            'origin': sender_origin, 
            'destination': sender_destination
        })
    
    def post(self, request, *args, **kwargs):
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        pnr_number = request.POST.get('pnr_number')
        sender_origin = request.POST.get('sender_origin')
        sender_destination = request.POST.get('sender_destination')

        print(f"Origin: {origin}, Destination: {destination}, PNR: {pnr_number}, SenderOrigin: {sender_origin}, SenderDestination: {sender_destination}")  # Debug output

        if not origin or not destination or not pnr_number:
            return JsonResponse({'message': 'All fields are required.'}, status=400)

        is_valid, message = verify_route(origin, destination, pnr_number, sender_origin, sender_destination)
        print(f"Validation Result: {is_valid}, Message: {message}")  # Debug output
        return JsonResponse({'message': message}, status=200 if is_valid else 400)
    
class ReviewRequestsView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'core/review_requests.html'
    context_object_name = 'messages'

    def get_queryset(self):
        # get messages where the current user is the recipient
        return Message.objects.filter(recipient=self.request.user)

class ConfirmTravelerView(LoginRequiredMixin, View):
    def post(self, request, message_id):
        # Get the message object
        message = get_object_or_404(Message, id=message_id)

        # Ensure the request user is the recipient of the message
        if message.recipient != request.user:
            return HttpResponseForbidden("You are not allowed to confirm this traveler.")

        # Get the parcel associated with the message
        parcel = message.parcel

        # Set the traveling_user to the sender of the message
        parcel.traveling_user = message.sender
        parcel.save()

        # create a notification for the traveler
        notification = Notification.objects.create(
            user=parcel.traveling_user,
            message=f'You have been confirmed as the traveler for the parcel: {parcel.description}'
        )

        # Delete the message after confirming
        message.delete()

        return redirect('review_requests')

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return redirect('user_page')

'''class ValidatePNRAndRouteView(View):
    def post(self, request, *args, **kwargs):
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        pnr_number = request.POST.get('pnr_number')

        if not origin or not destination or not pnr_number:
            return JsonResponse({'message': 'All fields are required.'}, status=400)

        is_valid, message = verify_route(origin, destination, pnr_number)
        return JsonResponse({'message': message}, status=200 if is_valid else 400)'''
from rest_framework import serializers
from core.models import Parcel, PNR, TravelDetails, Message, Notification
from .utils import isStationBetween

class TravelRequestSerializer(serializers.ModelSerializer):
    pnr_number = serializers.CharField(max_length=10)

    class Meta:
        model = TravelDetails
        fields = ['pnr_number', 'origin', 'destination', 'travel_date', 'parcel']

    def create(self, validated_data):
        travel = TravelDetails.objects.create(
            traveler=self.context['request'].user,
            **validated_data
        )
        parcel = validated_data['parcel']
        parcel.status = 'pending_review'
        parcel.save()
        return travel

class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ('id', 'description', 'weight', 'origin', 'destination', 'deadline', 'sender', 'traveling_user')

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ('sender', 'traveling_user', 'description', 'weight', 'origin', 'destination', 'deadline')

class PNRSerializer(serializers.ModelSerializer):
    class Meta:
        model = PNR
        fields = ["pnr_number", "is_valid"]
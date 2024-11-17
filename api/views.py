from django.shortcuts import render
from rest_framework import generics, permissions, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Parcel, PNR, TravelDetails
from .serializers import ParcelSerializer, DetailSerializer, TravelRequestSerializer, PNRSerializer
from .permissions import IsAuthorOrReadOnly
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import Http404

# Create your views here.
class ParcelAPIView(generics.ListCreateAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer

class DetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parcel.objects.all()
    serializer_class = DetailSerializer

class PNRList(generics.ListCreateAPIView):
    queryset = PNR.objects.all()
    serializer_class = PNRSerializer

    def post(self, request, *args, **kwargs):
        pnr_number = request.data.get('pnr_number')
        # check if the pnr already exists in the database
        pnr_instance = PNR.objects.filter(pnr_number=pnr_number).first()

        if pnr_instance:
            # Return the stored result if PNR already exists
            return Response({
                "pnr_number": pnr_instance.pnr_number,
                "is_valid": pnr_instance.is_valid,
                "message": "PNR already checked."
            }, status=status.HTTP_200_OK)

        # Validate the PNR
        is_valid = pnr_number.startswith('1') and len(pnr_number) == 10

        # Create a new PNR entry with the validation result
        new_pnr = PNR.objects.create(pnr_number=pnr_number, is_valid=is_valid)

        return Response({
            "pnr_number": new_pnr.pnr_number,
            "is_valid": new_pnr.is_valid,
            "message": "PNR checked and result saved."
        }, status=status.HTTP_201_CREATED)

class PNRDelete(generics.RetrieveDestroyAPIView):
    queryset = PNR.objects.all()
    serializer_class = PNRSerializer
    lookup_field = 'pnr_number'

    def delete(self, request, *args, **kwargs):
        # Retrieve and delete the PNR object
        pnr_instance = self.get_object()
        self.perform_destroy(pnr_instance)
        return Response({"message": f"PNR {pnr_instance.pnr_number} deleted successfully."}, status=204)

class BecomeTravelerView(APIView):
    def post(self, request, parcel_id):
        try:
            parcel = Parcel.objects.get(id=parcel_id)
        except Parcel.DoesNotExist:
            return Response({"error": "Parcel not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TravelRequestSerializer(data=request.data, context={'request': request, 'parcel': parcel})

        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Travel request submitted"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
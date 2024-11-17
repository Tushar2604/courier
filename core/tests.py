from django.test import TestCase
from .models import Parcel

# Create your tests here.
class ParcelModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Parcel.objects.create(sender='user_m', description='first parcel description here')

    def test_sender_content(self):
        parcel = Parcel.objects.get(id=1)
        expected_object_name = f'{parcel.sender}'
        self.assertEqual(expected_object_name, 'first parcel')

    def test_description_content(self):
        parcel = Parcel.objects.get(id=1)
        expected_object_name = f'{parcel.description}'
        self.assertEqual(expected_object_name, 'a description here')
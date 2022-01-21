from rest_framework import serializers
from .models import Listing, BookingInfo, Reservation

class ListingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Listing
		fields = ['listing_type', 'title', 'city', 'country']

class BookingInfoSerializer(serializers.ModelSerializer):
	listing = ListingSerializer(read_only=True)
	class Meta:
		model = BookingInfo
		fields = ['listing', 'price']

from rest_framework import serializers
from .models import Listing, BookingInfo, Reservation

class ListingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Listing
		fields = ['listing_type', 'title', 'city', 'country']

class BookingInfoSerializer(serializers.ModelSerializer):
	listing = ListingSerializer(read_only=True)
	hotel_room_type = serializers.ReadOnlyField(source='hotel_room_type.title')
	class Meta:
		model = BookingInfo
		fields = ['listing', 'hotel_room_type', 'price']



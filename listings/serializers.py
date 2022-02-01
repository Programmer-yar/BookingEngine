from rest_framework import serializers
from .models import Listing, BookingInfo, Reservation

class ListingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Listing
		fields = ['id', 'listing_type', 'title', 'city', 'country']

class BookingInfoSerializer(serializers.ModelSerializer):
	listing = ListingSerializer(read_only=True)
	hotel_room_type = serializers.ReadOnlyField(source='hotel_room_type.title')
	class Meta:
		model = BookingInfo
		fields = ['listing', 'hotel_room_type', 'price']

class ReservationSerializer(serializers.ModelSerializer):
	# price = serializers.ReadOnlyField(source='booking_info.price')
	# listing = serializers.ReadOnlyField(source='booking_info.listing')
	# room_type = serializers.ReadOnlyField(source='booking_info.hotel_room_type')
	booking_info = BookingInfoSerializer(read_only=True)
	class Meta:
		model = Reservation
		fields = ['booking_info', 'hotel_room']
from listings.models import BookingInfo, HotelRoom, HotelRoomType

# Final Queries
"""
- removes all listings with price above max price
- removes apartments booked in the given date range
"""
price_apartment_filter = BookingInfo.objects.filter(
	price__lt=350, listing__listing_type='apartment'
	).exclude(
	reservation_info__date_reserved__range=('2021-12-12', '2021-12-15')
	)

"""Queries ending in BookingInfo"""

"""Queries starting from HotelRoom"""
# gets available rooms
available_rooms = HotelRoom.objects.exclude(
	room_reservation_info__date_reserved__range=('2021-12-12', '2021-12-15')
	)

room_types = HotelRoomType.objects.filter(hotel_rooms__in=available_rooms)
hotels_info = BookingInfo.objects.filter(
				hotel_room_type__in=room_types,
				price__lt=350)

"""Queries ending in BookingInfo"""
available_listings = price_apartment_filter.union(hotels_info).order_by('price')



from listings.models import BookingInfo, HotelRoom, HotelRoomType
from listings.serializers import BookingInfoSerializer
serializer = BookingInfoSerializer()
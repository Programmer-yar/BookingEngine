from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import BookingInfo, HotelRoom, HotelRoomType
from .serializers import BookingInfoSerializer


@csrf_exempt
def available_listings(request, max_price, check_in, check_out):
    """
    gives available listing which are not booked in given price range
    """
    if request.method == 'GET':
    	price_apartment_filter = BookingInfo.objects.filter(
    		price__lt=max_price, listing__listing_type='apartment'
    		).exclude(
    		reservation_info__date_reserved__range=(check_in, check_out)
    		)
    	available_rooms = HotelRoom.objects.exclude(
    		room_reservation_info__date_reserved__range=(check_in, check_out)
    		)
    	room_types = HotelRoomType.objects.filter(
			    		hotel_rooms__in=available_rooms
			    		)
    	hotels_info = BookingInfo.objects.filter(
    					hotel_room_type__in=room_types, price__lt=max_price
    					)
    	available_listings = price_apartment_filter.union(hotels_info).order_by('price')
    	serializer = BookingInfoSerializer(available_listings, many=True)
    	return JsonResponse(serializer.data, safe=False)
		
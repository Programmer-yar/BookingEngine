from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins

from .models import BookingInfo, HotelRoom, HotelRoomType
from .serializers import BookingInfoSerializer


class ListingsFilter(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = BookingInfoSerializer

    def get(self, request, *args, **kwargs):
        """
        gives available listing which are not booked in given price range
        """
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        # Filtering against a URL by overriding 'get_queryset' method
        max_price = self.kwargs['max_price']
        check_in = self.kwargs['check_in']
        check_out = self.kwargs['check_out']
        price_apartment_filter = BookingInfo.objects.filter(
        price__lt=max_price, listing__listing_type='apartment').exclude(
        reservation_info__date_reserved__range=(check_in, check_out)
        )
        available_rooms = HotelRoom.objects.exclude(room_reservation_info__date_reserved__range=(check_in, check_out))
        room_types = HotelRoomType.objects.filter(
                        hotel_rooms__in=available_rooms
                        )
        hotels_info = BookingInfo.objects.filter(
                        hotel_room_type__in=room_types, price__lt=max_price
                        )
        available_listings = price_apartment_filter.union(hotels_info).order_by('price')
        return available_listings
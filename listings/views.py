from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics, mixins
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions

from .models import (Listing, BookingInfo, HotelRoom, HotelRoomType,
                     Reservation)
from .serializers import BookingInfoSerializer, ReservationSerializer
from .utils import (check_listings_availability, date_range,
                    check_specific_listing)

@api_view(['GET'])
def api_root(request, format=None):
    # Not working
    return Response({
        'available_listings': reverse('available_listings', request=request,
                                        format=format),
        })

class AllListings(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = BookingInfo.objects.all().order_by('price')
    serializer_class = BookingInfoSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class ListingsFilter(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = BookingInfoSerializer

    def get(self, request, *args, **kwargs):
        """gives available listing which are not booked in given price range"""
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        """Filtering against a URL by overriding 'get_queryset' method
        - See 'Filtering' topic in DRF docs
        """
        # max_price = self.kwargs['max_price']
        # check_in = self.kwargs['check_in']
        # check_out = self.kwargs['check_out']

        max_price = self.request.GET.get('max_price')
        check_in = self.request.GET.get('check_in')
        check_out = self.request.GET.get('check_out', check_in)
        available_listings = check_listings_availability(max_price, check_in, check_out)
        return available_listings

class Booking(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=format):
        reservations = Reservation.objects.filter(booked_by=self.request.user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request, format=format):
        user = request.user
        listing_id = request.data.get('listing_id')
        room_type = request.data.get('room_type')
        room_number = request.data.get('room_number')
        check_in = request.data.get('check_in')
        check_out = request.data.get('check_out', check_in)

        listing = get_object_or_404(Listing, pk=listing_id)
        available, room = check_specific_listing(
            listing, check_in, check_out, room_number, room_type)
        
        if available:
            booking_days = date_range(check_in, check_out)
            book_info = BookingInfo.objects.filter(listing=listing)[0]
            for day in booking_days:
                Reservation.objects.create(
                    booking_info=book_info, booked_by=user,
                    date_reserved=day, hotel_room=room)
            context = {
                "status": "Booking Successful",
                "check_in": check_in,
                "check_out": check_out,
                "total_days": len(booking_days),
                "Listing": listing.title,
                "room_type": room_type,
                "room_number": room_number
            }
            return Response(context, status=status.HTTP_201_CREATED)
        context = {
            "status": "Already Booked in given range!",
            "check_in": check_in,
            "check_out": check_out
        }
        return Response(context, status=status.HTTP_204_NO_CONTENT)
        



# sample inputs for booking
{
    "listing_id": 8,
    "room_number": 101,
    "room_type": "Single Bed",
    "check_in": "2022-01-19",
    "check_out": "2022-01-21"
}

{
    "listing_id": 6,
    "check_in": "2022-01-21",
}
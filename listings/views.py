from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import BookingInfo, HotelRoom, HotelRoomType
from .serializers import BookingInfoSerializer
from .utils import check_listing_availability

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
        check_out = self.request.GET.get('check_out')
        if not check_out: check_out = check_in
        available_listings = check_listing_availability(max_price, check_in, check_out)
        return available_listings
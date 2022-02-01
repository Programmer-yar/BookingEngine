from datetime import datetime, timedelta
from .models import Listing, BookingInfo, HotelRoom, HotelRoomType

def check_listings_availability(max_price, check_in, check_out):
    """ Provides a list of available hotel rooms/ apartments based on
    check_in, check_out dates
    """
    price_apartment_filter = BookingInfo.objects.filter(
        price__lt=max_price, listing__listing_type='apartment').exclude(
            reservation_info__date_reserved__range=(check_in, check_out))
    available_rooms = HotelRoom.objects.exclude(room_reservation_info__date_reserved__range=(check_in, check_out))
    room_types = HotelRoomType.objects.filter(
                    hotel_rooms__in=available_rooms)
    hotels_info = BookingInfo.objects.filter(
                    hotel_room_type__in=room_types, price__lt=max_price)
    available_listings = price_apartment_filter.union(hotels_info).order_by('price')
    return available_listings

def check_specific_listing(listing, check_in, check_out,
                            room_number, room_type):
    """Checks the availability of specific apartment/hotel_room
    in give date range
    """
    room = None
    if listing.listing_type == 'apartment':
        booking_info_obj = BookingInfo.objects.get(listing=listing)
        found = booking_info_obj.reservation_info.filter(
            date_reserved__range=(check_in, check_out))
    else:
        room_type_obj = HotelRoomType.objects.get(
            hotel=listing, title=room_type)
        room = HotelRoom.objects.get(hotel_room_type=room_type_obj,
                                     room_number=room_number)
        found = room_type_obj.booking_info.reservation_info.filter(
            date_reserved__range=(check_in, check_out),
            hotel_room__room_number=room_number)

    if found: return False, room
    return True, room

def date_range(check_in, check_out):
    start = datetime.strptime(check_in, "%Y-%m-%d")
    end = datetime.strptime(check_out, "%Y-%m-%d")
    delta = end - start  # as timedelta
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days
from django.db import models
from django.contrib.auth.models import User


class Listing(models.Model):
    HOTEL = 'hotel'
    APARTMENT = 'apartment'
    LISTING_TYPE_CHOICES = (
        ('hotel', 'Hotel'),
        ('apartment', 'Apartment'),
    )

    listing_type = models.CharField(
        max_length=16,
        choices=LISTING_TYPE_CHOICES,
        default=APARTMENT
    )
    title = models.CharField(max_length=255,)
    country = models.CharField(max_length=255,)
    city = models.CharField(max_length=255,)

    def __str__(self):
        return self.title
    

class HotelRoomType(models.Model):
    hotel = models.ForeignKey(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='hotel_room_types'
    )
    title = models.CharField(max_length=255,)

    def __str__(self):
        return f'{self.hotel} - {self.title}'


class HotelRoom(models.Model):
    hotel_room_type = models.ForeignKey(
        HotelRoomType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='hotel_rooms'
    )
    room_number = models.CharField(max_length=255,)

    def __str__(self):
        return self.room_number


class BookingInfo(models.Model):
    listing = models.ForeignKey(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='booking_info'
    )
    hotel_room_type = models.OneToOneField(
        HotelRoomType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='booking_info',
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        if self.hotel_room_type:
            obj = self.hotel_room_type
        else:
            obj = self.listing
            
        return f'{obj} {self.price}'


class Reservation(models.Model):
    booking_info = models.ForeignKey(
        BookingInfo,
        on_delete=models.CASCADE,
        related_name='reservation_info'
        )
    hotel_room = models.ForeignKey(
        HotelRoom,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='room_reservation_info'
        )
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_reserved = models.DateField()

    def __str__(self):
        if self.hotel_room:
            return f'Room {self.hotel_room} ({self.booking_info}) reserved for {self.date_reserved}'
        else:
            return f'{self.booking_info} reserved for {self.date_reserved}'


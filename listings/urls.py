from django.urls import path
from .views import ListingsFilter, AllListings, Booking

urlpatterns = [
	# 'api/v1/available-listings/<int:max_price>/<str:check_in>/<str:check_out>',
	path(
		'api/v1/available-listings', ListingsFilter.as_view(),
		name='available-listings'),
	path('api/v1/all-listings', AllListings.as_view(), name= 'all-listings'),
	path('api/v1/booking', Booking.as_view(), name='booking'),
	]

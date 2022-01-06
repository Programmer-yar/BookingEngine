from django.urls import path
from .views import available_listings

urlpatterns = [
	path(
		'available-listings/<int:max_price>/<str:check_in>/<str:check_out>',
		available_listings, name='available-listings'
		),
	]
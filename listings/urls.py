from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ListingsFilter

urlpatterns = [
	path(
		'available-listings/api/v1/<int:max_price>/<str:check_in>/<str:check_out>',
		ListingsFilter.as_view(), name='available-listings'
		),
	]

urlpatterns = format_suffix_patterns(urlpatterns)
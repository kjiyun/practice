from django.urls import path
from .views import FreeBoardListView

urlpatterns = [
    path('freecommunity_search/',FreeBoardListView.as_view({'get': 'get'}), name='freecommunity_search'),
]

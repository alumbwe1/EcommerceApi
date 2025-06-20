from django.urls import path
from .views import (
    EventListCreateAPIView,
    TicketListCreateAPIView,
    HostTicketListAPIView,
    TicketTypeListCreateAPIView,
    CategoryListCreateAPIView,
)

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('events/', EventListCreateAPIView.as_view(), name='event-list-create'),
    path('ticket-types/', TicketTypeListCreateAPIView.as_view(), name='ticket-type-list-create'),
    path('tickets/', TicketListCreateAPIView.as_view(), name='ticket-list-create'),
    path('host-tickets/', HostTicketListAPIView.as_view(), name='host-ticket-list'),
]

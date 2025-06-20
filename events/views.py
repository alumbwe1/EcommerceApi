from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Event, Ticket, TicketType, Category
from .serializers import EventSerializer, TicketSerializer, TicketTypeSerializer, CategorySerializer

# CATEGORY
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

# EVENT
class EventListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Event.objects.all()

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

# TICKET for logged-in users
class TicketListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# HOST TICKET (Only show tickets for events hosted by current user)
class HostTicketListAPIView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(event__host=self.request.user)

# TICKET TYPE
class TicketTypeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TicketTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TicketType.objects.filter(event__host=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

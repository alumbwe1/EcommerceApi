from rest_framework import viewsets, permissions
from .models import Event, Ticket, TicketType, Category
from .serializers import EventSerializer, TicketSerializer, TicketTypeSerializer, CategorySerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class HostTicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(event__host=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

class TicketTypeViewSet(viewsets.ModelViewSet):
    serializer_class = TicketTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TicketType.objects.filter(event__host=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
    def create(self, validated_data):
        event = validated_data['event']
        ticket_type = TicketType.objects.create(event=event, **validated_data)
        return ticket_type
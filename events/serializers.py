from rest_framework import serializers
from .models import Event, TicketType, Ticket, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['name', 'price', 'quantity_available', 'event']

class EventSerializer(serializers.ModelSerializer):
    ticket_types = TicketTypeSerializer(many=True, read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True
    )

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'location', 'image','ticket_type',
            'date', 'phone_number', 'ticket_types', 'category', 'age_restriction',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        request = self.context.get('request')
        ticket_types_data = self.initial_data.get('ticket_types', [])
        event = Event.objects.create(host=request.user, **validated_data)

        for ticket_type_data in ticket_types_data:
            TicketType.objects.create(event=event, **ticket_type_data)

        return event



class TicketSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()
    ticket_type_id = serializers.PrimaryKeyRelatedField(queryset=TicketType.objects.all(), source='ticket_type', write_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'ticket_number', 'ticket_type_id', 'payment_method', 'status', 'qr_code_url']
        read_only_fields = ['id', 'ticket_number', 'status', 'qr_code_url']

    def get_qr_code_url(self, obj):
        return obj.qr_code.url if obj.qr_code else None

    def create(self, validated_data):
        user = self.context['request'].user
        ticket_type = validated_data['ticket_type']
        if ticket_type.quantity_available <= 0:
            raise serializers.ValidationError("No tickets left for this type.")
        ticket_type.quantity_available -= 1
        ticket_type.save()
        return Ticket.objects.create(user=user, event=ticket_type.event, **validated_data)
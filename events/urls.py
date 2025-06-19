from rest_framework.routers import DefaultRouter
from .views import EventViewSet, TicketTypeViewSet, TicketViewSet, HostTicketViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'events', EventViewSet, basename='event')
router.register(r'ticket-types', TicketTypeViewSet, basename='ticket-type')
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'host-tickets', HostTicketViewSet, basename='host-ticket')

urlpatterns = router.urls

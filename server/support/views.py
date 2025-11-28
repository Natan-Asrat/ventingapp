from rest_framework import viewsets, mixins
from .models import Contact
from .serializers import ContactSerializer
# Create your views here.
class ContactViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
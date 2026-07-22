from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from categories.models import Category
from categories.api.serializers import CategorySerializer
from categories.api.permissions import IsAdminOrReadOnly

class CategoryViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Category.objects.filter(published=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('published', 'title')

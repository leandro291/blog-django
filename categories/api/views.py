from categories.models import Category
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from categories.api.serializers import CategoryReadSerializer, CategoryWriteSerializer
from categories.api.permissions import IsAdminOrReadOnly

class CategoryViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Category.objects.filter(published=True)
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('published', 'title')

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return CategoryWriteSerializer

        return CategoryReadSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Category.objects.all()

        return Category.objects.filter(published=True)

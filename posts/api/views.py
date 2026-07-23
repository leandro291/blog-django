from rest_framework.viewsets import ModelViewSet
from posts.api.serializers import PostReadSerializer, PostWriteSerializer
from posts.models import Post
from posts.api.permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class PostViewSet(ModelViewSet):
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__slug', 'category']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return PostWriteSerializer

        return PostReadSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all().select_related('user', 'category')

        return Post.objects.filter(published=True).select_related('user', 'category')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

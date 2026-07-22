from rest_framework.viewsets import ModelViewSet
from posts.api.serializers import PostSerializer
from posts.models import Post
from posts.api.permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class PostViewSet(ModelViewSet):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__slug', 'category']

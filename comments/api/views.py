from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from comments.models import Comment
from comments.api.serializers import CommentWriteSerializer, CommentReadSerializer
from comments.api.permissions import IsOwnerOrReadAndCreateOnly

class CommentViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadAndCreateOnly]
    queryset = Comment.objects.all().select_related('user', 'post')
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering = ('-created_at',)
    filterset_fields = ('post',)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return CommentWriteSerializer

        return CommentReadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

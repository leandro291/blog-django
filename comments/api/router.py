from rest_framework.routers import DefaultRouter

from comments.api.views import CommentViewSet

router_comments = DefaultRouter()

router_comments.register('comments', CommentViewSet, basename='comments')

from rest_framework.routers import DefaultRouter

from posts.api.views import PostViewSet

router_posts = DefaultRouter()

router_posts.register('posts', PostViewSet, basename='posts')
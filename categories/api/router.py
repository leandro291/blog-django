from rest_framework.routers import DefaultRouter
from categories.api.views import CategoryViewSet

router = DefaultRouter()

router.register('categories', CategoryViewSet, 'categories')


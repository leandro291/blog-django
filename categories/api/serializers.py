from categories.models import Category
from rest_framework.serializers import ModelSerializer

class CategoryWriteSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'slug')

class CategoryReadSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'slug', 'published')
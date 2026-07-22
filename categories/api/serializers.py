from categories.models import Category
from rest_framework.serializers import ModelSerializer

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id' ,'title', 'slug', 'published')
from rest_framework.relations import PrimaryKeyRelatedField

from categories.models import Category
from posts.models import Post
from rest_framework.serializers import ModelSerializer
from users.api.serializers import UserSerializer

class PostWriteSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content', 'miniature', 'category', 'published', 'slug')

class PostReadSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    category = PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'miniature', 'published', 'created_at', 'category', 'slug')

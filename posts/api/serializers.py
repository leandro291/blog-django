from posts.models import Post
from rest_framework.serializers import ModelSerializer

from users.api.serializers import UserSerializer
from categories.api.serializers import CategorySerializer

class PostWriteSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content', 'miniature', 'category', 'published', 'slug')

class PostReadSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'miniature', 'published', 'created_at', 'category', 'slug')

from rest_framework.serializers import ModelSerializer
from posts.models import Post
from users.api.serializers import UserSerializer
from categories.api.serializers import CategorySerializer


class PostSerializer(ModelSerializer):

    user = UserSerializer()
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'miniature', 'published', 'created_at', 'category', 'slug')

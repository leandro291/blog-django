from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from comments.models import Comment

from users.api.serializers import UserSerializer

class CommentWriteSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ('content', 'post')

class CommentReadSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)
    post = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'content', 'created_at')


from users.models import User
from rest_framework.viewsets import ModelViewSet
from users.api.serializers import UserSerializer

class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
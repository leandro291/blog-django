from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from users.api.serializers import UserRegisterSerializer, UserSerializer, UserUpdateSerializer


class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UserUpdateSerializer
        return UserSerializer
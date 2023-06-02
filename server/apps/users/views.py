from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView, Request
from rest_framework_simplejwt.tokens import RefreshToken

from server.apps.users import exceptions, serializers
from server.core.auth.permissions import IsAuthenticated

User = get_user_model()


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView,
):
    """User patch/get/delete viewset."""

    permission_classes = (IsAuthenticated,)

    queryset = User.objects.filter(is_staff=False, is_superuser=False)
    serializer_class = serializers.UserSerializer

    def get(self, request, *args, **kwargs):
        """Get current user account."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """Patch user account."""
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(user, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            user._prefetched_objects_cache = {}  # noqa: WPS437

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        """Delete user account."""
        self.perform_destroy(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(APIView):
    """User register view."""

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=serializers.RegistrationSerializer,
        responses={'201': serializers.AuthenticatedUserSerializer()},
    )
    def post(self, request: Request, *args, **kwargs):
        """Register user method."""
        serializer = serializers.RegistrationSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.create_user(**serializer.data)
        except exceptions.UserAlreadyJoined:
            raise exceptions.UserExist()

        token = RefreshToken.for_user(user)
        data = {
            'user': user,
            'tokens': {
                'refresh': str(token),
                'access': str(token.access_token),
            },
        }
        return Response(
            data=serializers.AuthenticatedUserSerializer(data).data,
            status=status.HTTP_201_CREATED,
        )


class LogoutView(APIView):
    """User logout view."""

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=serializers.LogoutSerializer,
    )
    def post(self, request, *args, **kwargs):
        """Logout user and reset tokens."""
        access = request.auth
        refresh = serializers.LogoutSerializer(
            data=request.data,
            context={'request': request},
        )
        self._reset_token(access)
        self._reset_token(refresh)
        return Response(status=status.HTTP_205_RESET_CONTENT)

    def _reset_token(self, token):
        """Blacklist token."""
        try:
            token.blacklist()
        except AttributeError:
            pass  # noqa: WPS420

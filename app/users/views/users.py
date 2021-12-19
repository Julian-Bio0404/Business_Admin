"""Users views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from app.users.models import User

# Serializers
from app.users.serializers import (
    AccountVerificationSerializer,
    RestorePasswordSerializer,
    TokenRestorePasswordSerializer,
    UpdatePasswordSerializer,
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer
)


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    User view set.
    Handle signup, login, account verification, refresh 
    token, update email, restore and update password.
    """

    queryset = User.objects.filter(verified=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data, 'access_token': token}
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Congratulations, now you can login and update some data and password.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def token_restore_psswd(self, request):
        """Create a token for restore password."""
        serializer = TokenRestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'message': 'We have sent an email for you to reset your password.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def restore_psswd(self, request):
        """Restore user's password."""
        serializer = RestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Your password has been reset.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def update_psswd(self, request, *args, **kwargs):
        """Update user's password."""
        serializer = UpdatePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Your password has been updated.'}
        return Response(data, status=status.HTTP_200_OK)
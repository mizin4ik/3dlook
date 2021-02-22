from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from users.models import User


class UserRegisterSerializer(RegisterSerializer):
    birthday = serializers.DateField(required=False)
    avatar = serializers.ImageField(required=False)

    def custom_signup(self, request, user):
        """Save birthday and avatar when user register."""
        if birthday := request.data.get('birthday'):
            user.birthday = birthday
        if avatar := request.data.get('avatar'):
            user.avatar = avatar
        user.full_clean()
        user.save()


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk', 'username', 'email', 'first_name',
            'last_name', 'avatar', 'birthday'
        )
        read_only_fields = ('email',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

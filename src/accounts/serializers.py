from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from accounts.models import CustomUser


class AccountsCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        )

    def save(self):
        password = self.validated_data['password']
        user = CustomUser.objects.create(**self.validated_data)
        user.set_password(password)
        user.save()
        self.token = Token.objects.create(user=user)
        return self.validated_data

    def to_representation(self, validated_data):
        return {
            'key': self.token.key
        }


class AccountsLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, max_length=150)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=True)


    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not attrs.get('username') and not attrs.get('email'):
            raise serializers.ValidationError('Username OR email required.')
        if attrs.get('username') and attrs.get('email'):
            raise serializers.ValidationError('ONLY Username OR email.')

        username_or_email = 'email' if attrs.get('email') else 'username'
        kwargs = {username_or_email: attrs[username_or_email]}
        
        try:
            self.user = CustomUser.objects.get(**kwargs)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Username or email nonexistent.')

        if not self.user.check_password(attrs['password']):
            raise serializers.ValidationError('Invalid username/email or password')

        return attrs

    def create(self, validated_data):
        self.token, _ = Token.objects.get_or_create(user=self.user)
        return self.token

    def to_representation(self, validated_data):
        return {
            'key': self.token.key
        }

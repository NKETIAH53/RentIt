from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from djoser.serializers import UserCreateSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='profile.gender')
    phone_number = PhoneNumberField(source='profile.phone_number')
    profile_photo = serializers.ImageField(source='profile.profile_photo')
    country = CountryField(source='profile.country')
    city = serializers.CharField(source='profile.city')
    top_seller = serializers.BooleanField(source='profile.top_seller')
    full_name = serializers.SerializerMethodField(source='get_full_name')
    firstname = serializers.SerializerMethodField()
    firstname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'firstname',
            'lastname',
            'full_name',
            'gender',
            'phone_number',
            'profile_photo',
            'country',
            'city',
            'top_seller',
        ]

    def get_firstname(self, obj):
        return f'{obj.firstname.title()}'
    
    def get_lastname(self, obj):
        return f'{obj.lastname.title()}'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_superuser:
            representation['admin'] = True
        elif instance.is_active:
            representation['account_active'] = False

        return representation


class CreateUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = [
            'id',
            'username',
            'email',
            'firstname',
            'lastname',
            'password'
        ]

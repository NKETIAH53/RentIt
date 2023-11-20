from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from apps.ratings.serializers import RatingSerializer
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    firstname = serializers.CharField(source='user.firstname')
    lastname = serializers.CharField(source='user.lastname')
    email = serializers.EmailField(source='user.email')
    full_name = serializers.CharField(source='user.get_full_name')
    country = CountryField(name_only=True)
    ratings = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'username',
            'firstname',
            'lastname',
            'full_name',
            'email',
            'id',
            'phone_number',
            'profile_photo',
            'bio',
            'license',
            'gender',
            'country',
            'city',
            'is_buyer',
            'is_seller',
            'is_agent',
            'rating',
            'num_reviews',
            'ratings'
        ]

    def get_ratings(self, obj):
        ratings = obj.agent_rating.all()
        serializer = RatingSerializer(ratings, many=True)
        return serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.top_agent:
            representation['top_agent'] = True
        return representation
    

class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            'phone_number',
            'profile_photo',
            'bio',
            'gender',
            'country',
            'city',
            'is_buyer',
            'is_seller',
            'is_agent',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.top_agent:
            representation['top_agent'] = True
        return representation

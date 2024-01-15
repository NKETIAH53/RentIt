from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import Property, PropertyViews


class PropertySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    country = CountryField(name_only=True)
    cover_image = serializers.SerializerMethodField()
    secondary_image1 = serializers.SerializerMethodField()
    secondary_image2 = serializers.SerializerMethodField()
    secondary_image3 = serializers.SerializerMethodField()
    secondary_image4 = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            "id",
            "user",
            "title",
            "slug",
            "reference_code",
            "description",
            "country",
            "city",
            "digital_address",
            "price",
            "property_dimensions",
            "advert_type",
            "property_type",
            "cover_image",
            "secondary_image1",
            "secondary_image2",
            "secondary_image3",
            "secondary_image4",
            "is_published",
            "views",
        ]

    def get_user(self, obj):
        return obj.user.username

    def get_cover_image(self, obj):
        return obj.cover_image.url

    def get_secondary_image1(self, obj):
        return obj.secondary_image1.url

    def get_secondary_image2(self, obj):
        return obj.secondary_image2.url

    def get_secondary_image3(self, obj):
        return obj.secondaryimage3.url

    def get_secondary_image4(self, obj):
        return obj.secondary_image4.url


class PropertyCreateSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Property
        exclude = ["modified_at", "pkid"]


class PropertyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyViews
        exclude = ["modified_at", "pkid"]

from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField(read_only=True)
    agent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rating
        exclude = ['modified_at', 'pkid']
        fields = [
            'client',
            'agent',
            'rating',
            'comment'
        ]

    def get_client(self, obj):
        return obj.client.username
    
    def get_agent(self, obj):
        return obj.agent.user.username

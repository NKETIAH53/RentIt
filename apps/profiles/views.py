from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .exceptions import NotYourProfile, ProfileNotFound
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer, UpdateProfileSerializer
from rest_framework.decorators import api_view, permission_classes


class AgentListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(is_agent=True)
    serializer_class = ProfileSerializer


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def get_all_top_agents(request):
    top_agents = Profile.objects.filter(top_agent=True)
    serializer = ProfileSerializer(top_agents, many=True)
    return Response({'top_agents': serializer.data}, status=status.HTTP_200_OK)


class UserProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]

    def get(self, request):
        user = self.request.user
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProfileUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = UpdateProfileSerializer

    def patch(self, request, username):
        try:
            Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileNotFound
        
        if (user_name := username) != username:
            raise NotYourProfile
        
        data = request.data
        serializer = UpdateProfileSerializer(
            instance=request.user.profile,
            data=data,
            partial=True
        )
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
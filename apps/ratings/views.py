from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.profiles.models import Profile
from .models import Rating


User = get_user_model()


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def agent_review(request, profile_id):
    data = request.data
    agent_profile = Profile.objects.get(id=profile_id, is_agent=True)

    if request.user == agent_profile.user:
        return Response(
            {'message': 'You cannot rate yourself as an agent.'},
            status=status.HTTP_403_FORBIDDEN
        )

    already_rated = Rating.objects.filter(client=request.user, agent=agent_profile).exists()

    if already_rated:
        return Response(
            {'message': 'This agent has already been rated.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    elif data['rating'] == 0:
        return Response(
            {'message': 'Please select a rating.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    rating = Rating.objects.create(
        client=request.user,
        agent = agent_profile,
        rating=data['rating'],
        comment=data['comment']
    )
    reviews = agent_profile.agent_rating.all()
    agent_profile.num_reviews = len(reviews)

    total_ratings = 0
    for review in reviews:
        total_ratings += review.rating

    return Response(f'Review added to agent {agent_profile.user.username}')
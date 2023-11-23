import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .exceptions import PropertyNotFound
from .models import Property, PropertyViews
from .pagination import PropertyPagination
from .serializers import PropertyCreateSerializer, PropertySerializer, PropertyViewSerializer
from .filters import PropertyFilter


logger = logging.getLogger(__name__)


class PropertiesListAPIView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all().order_by('-created_at')
    pagination_class = PropertyPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    filterset_class= PropertyFilter
    search_fields = [
        'country',
        'city'
    ]
    ordering_fields = [
        'created_at'
    ]

    def create(self, request):
        user = request.user
        data = request.data
        data['user'] = user.pkid

        serializer = PropertyCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info(
                f"New Property with name {serializer.data.get('title')} added by {user.username}"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyDetailAPIView(generics.DestroyAPIView):
    def get(self, request, slug):
        try:
            property = Property.objects.get(slug=slug)
        except Property.DoesNotExist:
            raise PropertyNotFound
        
        if (x_forwarded_for := request.META.get('HTTP_X_FORWARDED_FOR')):
            ip = x_forwarded_for.split(',')[0]
        ip = request.META.get('REMOTE_ADDR')

        if not PropertyViews.objects.filter(property=property, ip=ip).exists():
            PropertyViews.objects.create(property=property, ip=ip)
            property.views += 1
            property.save()

        serializer = PropertySerializer(property, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, slug):
        try:
            property = Property.objects.get(slug=slug)
        except Property.DoesNotExist:
            raise PropertyNotFound

        if (user := request.user) != property.user:
            return Response(
                {'error': 'You cannot delete a property you do not own.'}
            )
        
        data = {}
        deleted_property = property.delete()
        if deleted_property:
            data['success'] = f"Property {property.title} was successfully deleted"
            return Response(data, status.HTTP_200_OK)
        
        data['fail'] = f"Unable to delete Property, {property.title}"
        return Response(data, status.HTTP_400_BAD_REQUEST)


class AgentPropertyListAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    filterset_class= PropertyFilter
    search_fields = [
        'country',
        'city'
    ]
    ordering_fields = [
        'created_at'
    ]

    def get_queryset(self):
        user = self.request.user
        queryset = Property.objects.filter(user=user).order_by('-created_at')
        return queryset
    

class PropertyViewsAPIView(generics.ListAPIView):
    serializer_class = PropertyViewSerializer
    queryset = PropertyViews.objects.all()

        

@api_view(['PUT', 'PATCH'])
@permission_classes((permissions.IsAuthenticated,))
def update_property(request, slug):
    try:
        property = Property.objects.get(slug=slug)
    except Property.DoesNotExist:
        raise PropertyNotFound
    
    if (user := request.user) != property.user:
        return Response(
            {'error': 'You cannot update a property that does not belong to you.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = PropertySerializer(property, request.data, many=False, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def upload_property_image(request, slug):
    

    property = Property.objects.get(slug=slug)
    property.cover_image = request.FILES.get('cover_image', None)
    property.secondary_image1 = request.FILES.get('secondary_image1', None)
    property.secondary_image2 = request.FILES.get('secondary_image2', None)
    property.secondary_image3 = request.FILES.get('secondary_image3', None)
    property.secondary_image4 = request.FILES.get('secondary_image4', None)
    property.save()

    return Response(f'New images uploaded for property, {property.title}')


class PropertySearchAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PropertyCreateSerializer

    def post(self,request):
        data = request.data
        queryset = Property.objects.filter(is_published=True)

        if (advert_type := data.get('advert_type')) and not None:
            queryset = queryset.filter(advert_type__iexact=advert_type)

        elif (property_type := data.get('property_type')) and not None:
            queryset = queryset.filter(property_type__iexact=property_type)

        elif (city := data.get('city')) and not None:
            queryset = queryset.filter(city__iexact=city)

        elif (price := data.get('price')) and not None:
            price_mapping = {
                'GHC0+': 0,
                'GHC50,000+': 50000,
                'GHC100,000+': 100000,
                'GHC200,000+': 200000,
                'GHC500,000+': 500000,
                'any': -1,
            }
            price = price_mapping.get(price)

            if price != -1:
                queryset = queryset.filter(price__gte=price)

        elif (keyword := data["keyword"]) and not None:
            queryset = queryset.filter(description__icontains=keyword)

        serializer = PropertySerializer(queryset, many=True)
        return Response(serializer.data)
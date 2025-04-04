from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from ..models import Berkeh, Location, Comment
from ..serializers import BerkehSerializer, CommentSerializer, LocationSerializer


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["city", "province"]
    search_fields = ["country", "province", "county", "city", "village", "district"]


class CommentViewSet(viewsets.ViewSet):
    @extend_schema(
        description="Create a new comment.",
        request=CommentSerializer,
        responses={201: CommentSerializer},
    )
    def create(self, request):
        """
        Public API to create a comment.
        """
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Retrieve all comments related to a specific Berkeh.",
        parameters=[
            OpenApiParameter(
                name="berkeh_id",
                required=True,
                description="ID of the Berkeh to retrieve comments for.",
                type=int,
            )
        ],
        responses={200: {}},
    )
    @action(detail=False, methods=["get"], url_path="by-berkeh")
    def get_comments_by_berkeh(self, request):
        """
        API to retrieve all comments related to a specific Berkeh.
        Requires `berkeh_id` as a query parameter.
        """
        berkeh_id = request.query_params.get("berkeh_id")
        if not berkeh_id:
            return Response(
                {"error": "berkeh_id query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comments = Comment.objects.filter(berkeh_id=berkeh_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BerkehViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Berkeh.objects.all().select_related("location").prefetch_related("photos")
    )
    serializer_class = BerkehSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["location__city", "location__province"]
    search_fields = ["name", "description"]

    @extend_schema(
        description="Generate the next available Berkeh code based on location id.",
        parameters=[
            OpenApiParameter(
                name="location_id",
                required=True,
                description="ID of the location to generate the Berkeh code for.",
                type=int,
            )
        ],
        responses={200: {}},
    )
    @action(detail=False, methods=["get"], url_path="generate-code")
    def generate_code(self, request):
        """API to generate the next available Berkeh code based on location id"""
        location_id = request.query_params.get("location_id")

        if not location_id:
            return Response(
                {"error": "Location id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Ensure location exists in Location
            location = Location.objects.get(pk=location_id)
            return Response(
                {"code": Berkeh.generate_code(location)},
                status=status.HTTP_200_OK,
            )

        except Location.DoesNotExist:
            return Response(
                {"error": "Location not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

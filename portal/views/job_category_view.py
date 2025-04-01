from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from portal.models.job_category_model import JobCategory
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from portal.serializers.job_category_serializer import JobCategorySerializer
from ..utility.pagination import Pagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


@extend_schema(
    tags=['Job Category'],
    summary='List of all job categories',
    responses={200: JobCategorySerializer(many=True)},
    auth=[]
)
class JobCategoryListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    pagination_class = Pagination


@extend_schema(
    tags=['Job Category'],
    summary='Detail of a job category',
    responses={200: JobCategorySerializer},
    auth=[]
)
class JobCategoryDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    lookup_field = 'name'


class CreateJobCategoryView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = JobCategorySerializer

    @extend_schema(
        tags=['Job Category'],
        summary='Create new category (Admin Only)',
        responses={201: JobCategorySerializer}

    )
    def post(self, request):
        serializer = JobCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Category Successfully Added', 'result': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Job Category'],
    summary='Remove category (Admin Only)',
)
class RemoveJobCategoryView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    lookup_field = 'name'

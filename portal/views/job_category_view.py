from django.core.cache import cache
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from portal.models.job_category_model import JobCategory
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from portal.serializers.job_category_serializer import JobCategorySerializer
from ..utility.pagination import Pagination
from rest_framework.permissions import IsAdminUser, AllowAny


@extend_schema(
    tags=['Job Category'],
    summary='List of all job categories',
    responses={200: JobCategorySerializer(many=True)},
    auth=[]
)
class JobCategoryListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = JobCategorySerializer
    pagination_class = Pagination

    def get(self, request, *args, **kwargs):
        page = request.GET.get("page", 1)
        cache_key = f'job_category_list_page_{page}'

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        queryset = self.get_queryset()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = self.get_serializer(result_page, many=True)

        paginated_response = paginator.get_paginated_response(serializer.data)

        cache.set(cache_key, paginated_response.data, 60 * 15)

        return paginated_response

    def get_queryset(self):
        return JobCategory.objects.all()


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
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Category Successfully Added', 'result': serializer.data},
                        status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['Job Category'],
    summary='Remove category (Admin Only)',
)
class RemoveJobCategoryView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    lookup_field = 'name'

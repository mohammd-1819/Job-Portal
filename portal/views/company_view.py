from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from portal.models.company_model import Company
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from portal.serializers.company_serializer import CompanySerializer
from portal.models.job_owner_model import JobOwner
from ..utility.pagination import Pagination
from ..utility.permissions import IsJobOwner
from rest_framework.permissions import AllowAny


class CompanyListView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CompanySerializer
    pagination_class = Pagination

    @extend_schema(
        tags=['Company'],
        summary='List of all companies',
        responses={200: CompanySerializer(many=True)},
        auth=[]
    )
    def get(self, request):
        page = request.GET.get("page", 1)
        cache_key = f'company_list_page_{page}'

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        properties = Company.objects.all()
        paginator = self.pagination_class()
        result = paginator.paginate_queryset(properties, request, view=self)
        serializer = self.serializer_class(result, many=True, context={'request': request})

        paginated_response = paginator.get_paginated_response(serializer.data)

        cache.set(cache_key, paginated_response.data, 60 * 15)

        return paginated_response


class AddCompanyView(APIView):
    permission_classes = [IsJobOwner]
    serializer_class = CompanySerializer

    @extend_schema(
        tags=['Company'],
        summary='Add new Company',
        responses={201: CompanySerializer}
    )
    def post(self, request):
        owner = get_object_or_404(JobOwner.objects.select_related('user'), user=request.user)
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(owner=owner)
        return Response(
            {'message': 'Company successfully added', 'result': serializer.data},
            status=status.HTTP_201_CREATED
        )


class UpdateCompanyView(APIView):
    permission_classes = [IsJobOwner]
    serializer_class = CompanySerializer

    @extend_schema(
        tags=['Company'],
        summary='Update existing Company',
        responses={200: CompanySerializer}
    )
    def put(self, request, company_name):
        owner = get_object_or_404(JobOwner.objects.select_related('user'), user=request.user)
        company = get_object_or_404(Company.objects.select_related('owner'), name=company_name, owner=owner)
        serializer = self.serializer_class(instance=company, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Company Successfully Updated', 'result': serializer.data},
                        status=status.HTTP_200_OK)


class RemoveCompanyView(APIView):

    @extend_schema(
        tags=['Company'],
        summary='Remove Company',
    )
    def delete(self, request, company_name):
        owner = get_object_or_404(JobOwner.objects.select_related('user'), user=request.user)
        company = get_object_or_404(Company.objects.select_related('owner'), name=company_name, owner=owner)
        company.delete()
        return Response({'message': 'Company Removed'}, status=status.HTTP_200_OK)

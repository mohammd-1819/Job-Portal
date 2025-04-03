from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView
from portal.models.company_model import Company
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from portal.serializers.company_serializer import CompanySerializer
from portal.models.job_owner_model import JobOwner
from ..utility.pagination import Pagination
from ..utility.permissions import IsJobOwner
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


@extend_schema(
    tags=['Company'],
    summary='List of all companies',
    responses={200: CompanySerializer(many=True)},
    auth=[]
)
class CompanyListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = Pagination


class AddCompanyView(APIView):
    permission_classes = [IsJobOwner]
    serializer_class = CompanySerializer

    @extend_schema(
        tags=['Company'],
        summary='Add new Company',
        responses={201: CompanySerializer}
    )
    def post(self, request):
        owner = get_object_or_404(JobOwner, user=request.user)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(
                {'message': 'Company successfully added', 'result': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCompanyView(APIView):
    permission_classes = [IsJobOwner]
    serializer_class = CompanySerializer

    @extend_schema(
        tags=['Company'],
        summary='Update existing Company',
        responses={200: CompanySerializer}
    )
    def put(self, request, company_name):
        owner = get_object_or_404(JobOwner, user=request.user)
        company = get_object_or_404(Company, name=company_name, owner=owner)
        serializer = CompanySerializer(instance=company, data=request.data, partial=True)
        if serializer.is_valid():
            return Response({'message': 'Company Successfully Updated', 'result': serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveCompanyView(APIView):

    @extend_schema(
        tags=['Company'],
        summary='Remove Company',
    )
    def delete(self, request, company_name):
        owner = get_object_or_404(JobOwner, user=request.user)
        company = get_object_or_404(Company, name=company_name, owner=owner)
        company.delete()
        return Response({'message': 'Company Removed'}, status=status.HTTP_200_OK)
